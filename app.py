import gradio as gr
import os
import time
from pdf import generate_summary, generate_text, generate_answer

# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.

messages = []
current_file_text = None

def add_text(history, text):
    """
    TODO
    """
    history = history + [(text, None)]
    return history, gr.update(value="", interactive=False)


def add_file(history, file):
    """
    TODO
    """
    if file.name.endswith(".txt"):
        with open(file.name, "r", encoding="utf-8") as f:
            current_file_text = f.read()
            prompt = generate_summary(current_file_text)
    
    print("current_file_text: ", current_file_text)
    user_input = {"role": "user", "content": prompt}
    messages.append(user_input)
    history = history + [((file.name,), None)]
    return history


def bot(history):
    """
    TODO
    """
    content = str(messages[-1]["content"])
    
    if(content.startswith("Summarize")):
        response = generate_text(content)
    elif(content.startswith("/file")):
        messages[-1]["content"] = generate_answer(current_file_text, content)
        response = generate_text(messages[-1]["content"])
    
    history[-1][1] = response
    return history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        clear_btn = gr.Button('Clear')
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio", "text"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear_btn.click(lambda: messages.clear(), None, chatbot, queue=False)

demo.queue()
demo.launch()
