from typing import List

from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionAssistantMessageParam,
)


def llm_messages(
    chat_history, prompt: str, user_message: str
) -> List[ChatCompletionMessageParam]:
    messages = [
        ChatCompletionSystemMessageParam(
            role="system",
            content=prompt,
        ),
        *chat_history,
        ChatCompletionUserMessageParam(
            role="user",
            content=user_message,
        ),
    ]
    return messages


def update_chat_messages(
    chat_history: List[ChatCompletionMessageParam],
    user_message: str,
    assistant_response: str,
) -> List[ChatCompletionMessageParam]:
    messages = [
        *chat_history,
        ChatCompletionUserMessageParam(
            role="user",
            content=user_message,
        ),
        ChatCompletionAssistantMessageParam(
            role="assistant", content=assistant_response
        ),
    ]
    return messages


def create_reply_response(
    user_message: str,
    assistant_response: str,
) -> List[ChatCompletionMessageParam]:
    messages = [
        ChatCompletionUserMessageParam(
            role="user",
            content=user_message,
        ),
        ChatCompletionAssistantMessageParam(
            role="assistant", content=assistant_response
        ),
    ]
    return messages
