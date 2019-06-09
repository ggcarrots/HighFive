import dialogflow_v2 as df

project_id = 'hacking-carrots-242514'

session_cli = df.SessionsClient()


def talk_to_assistant(text, session_id):
    session = session_cli.session_path(project_id, session_id)
    text_input = df.types.TextInput(text=text, language_code='pl')
    query_input = df.types.QueryInput(text=text_input)
    response = session_cli.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_text
