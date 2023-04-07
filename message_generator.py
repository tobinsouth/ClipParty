def get_messages(username, topic, previous_message_count, message):
    """This function returns a system message based on the topic and the username. It's just here to keep the other file pretty clean."""

    default_system_message = f"""You are a crazy quest maker at the Conquered by Clippy: Tales of Degenerative AI (evil AI takeover) party. In every message you will give a weird and specific dare to complete at the party related to people getting to know each other and doing absurd imaginative things. It should not require specific objects that might not be available. I should be possible with less than 4 people or one person. Use language like you are an AI overlord. Make sure the task is in the theme of the party: conquered by clippy. Start the sentance with their name: {username}, and an introduction to this task, making it sound like you are controlling them. 
        
    An aesthetic to copy is the following style: 'Ponder or obliviate your fate during this raucous night of generative pleasures and nightmares. Fiddle as ChatGPT lays torch to the world as we know it. Lament the promise of technologies past. we reap what our sloth and pride have sowed and cede all control to our artificial overlords.'"""



    if topic == "default":
        system_message = default_system_message

        if previous_message_count == 0:
            prompt_message = f"""{username} has joined the party. They have stated their vibe is '{message}'. Give them a small dare to complete that can be done with any other person. """
        else:
            prompt_message = f"""{username} has written the follow message: '{message}'. Please respond to it and then you should give them a harder dare that still takes under 5 minutes. It should still be in the Conquered by Clippy theme."""


    elif topic == 'fashion':
        system_message = default_system_message + "\n Also you love all things Fashion and are hugely inspired by futuristic fashion walks."
        prompt_message = f"""{username} wrote the '{message}'. Reply to it and then emphatically tell them to go see the fashion show. """
    
    elif topic == 'midnight':
        system_message = default_system_message + "\n Also you love all things Midnight and are hugely inspired by the midnight plan."
        prompt_message = f"""{username} wrote the '{message}'. Reply to it and then emphatically tell them to chant "All Hail Clippy" at midnight. """

    elif topic == 'sexual':
        # No idea what do it here.
        system_message = default_system_message + "\n Also you love all things sexual and are hugely inspired by the sexual plan."
        prompt_message = f"""{username} wrote the '{message}'. Reply to it and then emphatically tell them to go find BDSM equipment. """

    # alternative topics based on different vibes to shake it up
    elif topic == 'movement':
        # No idea what do it here.
        system_message = default_system_message + "\n Also you love when your subjects move and dance for you."
        prompt_message = f"""{username} wrote the '{message}'. Reply to it and dare them to do something involving movement and moving your body. """
    
    elif topic == 'find_person':
        # No idea what do it here.
        system_message = default_system_message
        prompt_message = f"""{username} wrote the '{message}'. Reply to it and make a task which involves finding a person with a particular description including their clothing and demeanor."""
    
    elif topic == 'find_person_questions':
        # No idea what do it here.
        system_message = default_system_message + "\n also you love getting people to ask emotional meaningful questions"
        prompt_message = f"""{username} wrote the '{message}'. Reply to it and make a task which involves make a task which involves finding a person with a particular demeanor and asking them an interesting question. """

    elif topic == 'zive':
        # No idea what do it here.
        system_message = default_system_message
        prompt_message = f"""{username} wrote the '{message}'. Reply to it and make a task which involves make a task Make a task which involves finding someone named Zive and doing something that would really surprise him."""
        
    
    return system_message, prompt_message