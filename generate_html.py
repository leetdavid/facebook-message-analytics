import os
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def create_index_html(chat_data, metadata):
    fname = "output.html"
    context = {
        'totalSent': metadata['message_total_you'],
        'totalRecieved': metadata['message_total_other'],
        'conversationCount': metadata['individual_chat_count'],
        'groupChatCount': metadata['group_chat_count'],
        'chatMap': chat_data
    }
    with open(fname, 'w') as f:
        html = render_template('index.html', context)
        f.write(html)


#For testing
