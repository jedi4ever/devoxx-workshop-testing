# Devoxx Testing Workshop
## Requirements
### Github Codespaces
- The easiest way to run this repo is to run it in a Github Codespace
- For this you'll need a Github account. <https://github.com/signup>

### OpenAI API key
- The examples assume you have an `OPENAI_API_KEY` available.
- Signup via <https://platform.openai.com/api-keys>
- Make sure there is credit (~5-10 USD) in your account

- We'll configure this as a secret in the Github Codespace.
- When launching the codespace it will ask for the key.

### Running locally
- The setup assumes you have a working VSCode environment.
- A running docker container system. You can install <https://rancherdesktop.io/> if you don't have one.
- Make sure to have enough bandwith to pull images from. Therefore not ideal to do this at conferences :)

- Secrets should go into `.env` file:
    - `OPENAI_API_KEY="...."`
- In VSCode this .env is loaded automatically

### Launching the codespace
- Lauching the link below will spin up a webbased VSCode with Github Copilot enabled
- To use experimental Copilot features you can switch to the Insiders Version
- It will take a while to spin up.....
- You can watch the progress by clicking `Building codespace` in the lower right corner.
- After the installation process is finished, it's best to reload the editor: in the menu use `> View > Command Pallete > Developer Reload Window`

- [Launch in Codespace](https://github.com/codespaces/new/jedi4ever/devoxx-workshop-testing)
- Don't forget to remove the codespace after the workshop. <https://github.com/codespaces/>
