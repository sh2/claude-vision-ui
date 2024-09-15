import PIL.Image
import anthropic
import base64
import httpx
import io
import os
import streamlit as st


def main():
    anthropic_proxy = os.environ.get("ANTHROPIC_PROXY", "")
    http_client = None

    if anthropic_proxy:
        http_client = httpx.Client(proxies={"https://": anthropic_proxy})

    anthropic_client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY", ""), http_client=http_client)

    st.title("Claude 3 Vision UI")

    model_options = [
        "claude-3-5-sonnet-20240620",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]

    anthropic_model = st.selectbox("Language Model", model_options)

    if not anthropic_model:
        anthropic_model = model_options[0]

    files = st.file_uploader(
        "Please upload image files", accept_multiple_files=True, type=["jpeg", "jpg", "png"])

    if files:
        # Display image files in two columns
        columns = st.columns(2)
        column_index = 0

        for file in files:
            columns[column_index].image(file)
            column_index = (column_index + 1) % 2

    clear = st.button("Clear Chat History")

    if clear or "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept messages from the user
    if prompt := st.chat_input("Please enter a question about the images"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        messages_with_images = []
        response = ""

        # Display user's message
        with st.chat_message("user"):
            st.markdown(prompt)

        # For the assistant, display an empty message and update it later
        with st.chat_message("assistant"):
            message_assiatant = st.empty()

        # For the first message, change the format so that images can be attached
        messages_with_images.append({
            "role": st.session_state.messages[0]["role"],
            "content": []
        })

        # Attach images to the first message
        if files:
            index = 0

            for file in files:
                index += 1
                image = PIL.Image.open(file).convert("RGB")
                image.thumbnail((1568, 1568))

                with io.BytesIO() as buffer:
                    image.save(buffer, format="JPEG")
                    image_base64 = base64.b64encode(
                        buffer.getvalue()).decode("utf-8")

                messages_with_images[0]["content"].append({
                    "type": "text",
                    "text": f"Image {index}:"
                })

                messages_with_images[0]["content"].append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_base64
                    }
                })

        # Add the first message
        messages_with_images[0]["content"].append(
            {"type": "text", "text": st.session_state.messages[0]["content"]})

        # Add the second and subsequent messages as they are
        for message in st.session_state.messages[1:]:
            messages_with_images.append(message)

        with anthropic_client.messages.stream(
            max_tokens=4096,
            messages=messages_with_images,
            model=anthropic_model
        ) as stream:
            for response_chunk in stream.text_stream:
                response += response_chunk
                message_assiatant.markdown(response + "▌")

        message_assiatant.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
