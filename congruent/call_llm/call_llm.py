import os
from openai import OpenAI

from congruent.chat_history.redis import (
    retrieve_dialogue,
    store_dialogue,
)
from .llm_messages import llm_messages
from .llm_messages import llm_messages
from groq import Groq, AsyncGroq


api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
api_key_groq = os.getenv("GROQ_API_KEY")
client_groq_async = AsyncGroq(api_key=api_key_groq)
client_groq = Groq(api_key=api_key_groq)


def call_llm(
    prompt, 
    chat_history,
    user_query,
    tools=None,
    model="gpt-4o-mini",
    temperature=0.0,
    max_tokens=1000,
    tool_choice="auto",
):
    try:
        messages = llm_messages(chat_history, prompt, user_query)
        if tools:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,  # type: ignore
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
        else:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"},
            )
        return response.choices[0].message.content
    except Exception as e:
        print("Error in call_llm: ", e)
        raise e


def call_llm_groq_stream(
    prompt,
    user_query,
    session_id,
    model="llama-3.1-70b-versatile",
):
    try:
        previous_messages = retrieve_dialogue(session_id)
        messages = llm_messages(
            chat_history=previous_messages, prompt=prompt, user_message=user_query
        )

        stream = client_groq.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            max_tokens=1000,
            stream=True,
        )

        accumulated_text = ""
        total_text = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                token = chunk.choices[0].delta.content
                accumulated_text += token

                if token in ".!?" or len(accumulated_text) > 50:
                    total_text += accumulated_text
                    yield accumulated_text
                    accumulated_text = ""

        if accumulated_text:
            total_text += accumulated_text

            yield accumulated_text
        store_dialogue(
            session_key=session_id,
            query=user_query,
            reply=total_text,
            dialogue=previous_messages,
        )

    except Exception as e:
        print("Error in call_llm: ", e)
        raise e
