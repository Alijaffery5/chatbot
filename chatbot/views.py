import uuid
from datetime import *
from pytz import timezone
from datetime import datetime
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from .serializers import ChatSerializer

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Chat
from .utils import generate_response
from rest_framework import status

from functools import wraps
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes

# Decorator function for authentication based on Session and Token
def authenticated_view(view_func):
    @wraps(view_func)
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapped_view

# Function to format the DateTime
def format_time(dt):
    pst_tz = timezone('Asia/Karachi')
    # Set the timezone for PST
    """ Helper function to format datetime to PST with 'DD/MM/YYYY HH:MM:SS' format. """
    if dt:
        pst_time = dt.astimezone(pst_tz)
        return pst_time.strftime('%d/%m/%Y %H:%M:%S')
    return None


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found", }, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"message": "Logged-In successfully!", "token": token.key, "user": serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"message": "Registered successfully!", "token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authenticated_view
def test_token(request):
    return Response({"Passed for {}".format(request.user.email)})

@api_view(['GET', 'POST'])  # Allow both GET and POST methods
@authenticated_view
def chat_operations(request):
    if request.method == 'POST':
        # Retrieve content and end_session from the request
        content = request.data.get('content')
        end_session = request.data.get('end_session', False)  # Default to False if not provided

        # Convert end_session to a boolean if it is not already
        if isinstance(end_session, str):  # If it comes as a string, convert to boolean
            end_session = end_session.lower() in ['true', '1', 'yes']
        elif isinstance(end_session, int):  # If it comes as an integer (0 or 1)
            end_session = bool(end_session)

        # Check if content is provided
        if not content:
            return Response({'error': 'Content is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the latest chat for the current user
        last_chat = Chat.objects.filter(user=request.user).order_by('-start_time').first()

        pst_tz = timezone('Asia/Karachi')

        # If end_session is True, end the current chat session without creating a new entry
        if end_session:
            if last_chat and not last_chat.end_time:  # Ensure the chat hasn't been ended already
                last_chat.end_time = datetime.now()  # Set the end time for the chat
                last_chat.save()  # Save changes
                return Response({
                    'message': 'Chat session ended successfully.',
                    'start_time': format_time(last_chat.start_time),
                    'end_time': format_time(last_chat.end_time),
                    'session_id': last_chat.session_id
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No active chat session found to end.'}, status=status.HTTP_404_NOT_FOUND)

        # If end_session is False, continue the existing chat or create a new one if needed
        if last_chat and not last_chat.end_time:
            # Append the new user input to the existing chat content
            chatbot_response = generate_response(content)
            chat_content = last_chat.content

            # Update chat content with the new message
            chat_content.append({
                'message_id': str(uuid.uuid4()),  # Assign a unique identifier for each message
                "You": content,
                "Bot": chatbot_response,
                "timestamp": format_time(datetime.now())
            })

            # Save the updated chat content
            last_chat.content = chat_content
            last_chat.save()

            # Return the updated chat response
            return Response(ChatSerializer(last_chat).data, status=status.HTTP_200_OK)
        else:
            # Create a new chat session if no active session exists
            session_id = str(uuid.uuid4())  # Generate a new session ID
            chatbot_response = generate_response(content)

            # Initialize the chat content with the first message
            chat_content = [{
                'message_id': str(uuid.uuid4()),  # Assign a unique identifier for the message
                "You": content,
                "Bot": chatbot_response,
                "timestamp": format_time(datetime.now())
            }]

            # Create a new chat
            new_chat = Chat.objects.create(
                user=request.user,
                content=chat_content,
                session_id=session_id
            )

            # Return the new chat response
            return Response(ChatSerializer(new_chat).data, status=status.HTTP_201_CREATED)

    # Get the entire chat history or get by session_id using query params
    elif request.method == 'GET':
        # Retrieve session_id from query parameters (if provided)
        session_id = request.query_params.get('session_id')

        if session_id:
            # Filter chats by session_id for the authenticated user
            chats = Chat.objects.filter(user=request.user, session_id=session_id)
        else:
            # Retrieve all chat history for the authenticated user
            chats = Chat.objects.filter(user=request.user)
        data = [
            {
                'chat_id': chat.id,
                'start_time': format_time(chat.start_time),
                'end_time': format_time(chat.end_time),
                'content': chat.content,
                'session_id': chat.session_id
            } for chat in chats
        ]
        return Response(data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@authenticated_view
def update_message(request, chat_id, message_id):
    try:
        # Extract the message ID and new content from the request
        new_content = request.data.get('content')  # The new content for the message

        # Check if new_content and message_id are provided
        if not message_id or new_content is None:
            return Response({'error': 'Message ID and new content are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the chat object for the authenticated user
        chat = Chat.objects.get(id=chat_id, user=request.user)
        # Find the specific message in the chat content to update
        for message in chat.content:
            if message.get('message_id') == message_id:  # Match the message by ID
                message['You'] = new_content  # Update the message content
                break
        else:
            return Response({'error': 'Message not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Save the updated chat content back to the database
        chat.save()

        return Response({'message': 'Message updated successfully.'}, status=status.HTTP_200_OK)
    except Chat.DoesNotExist:
        return Response({'error': 'Chat not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@authenticated_view
def delete_chat(request, chat_id):
    try:
        # Try to get the chat instance for the authenticated user
        chat = Chat.objects.get(id=chat_id, user=request.user)
        chat.delete()  # Delete the chat instance
        return Response({'message': 'Chat deleted successfully.'},
                        status=status.HTTP_204_NO_CONTENT)  # Return success message with no content status
    except Chat.DoesNotExist:
        # Return a detailed error message if the chat is not found
        return Response({'error': 'Chat not found or you do not have permission to delete it.'},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Return a generic error message for any other exceptions
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
