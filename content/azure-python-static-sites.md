---
title: Deploying a Custom Python Static Site Generator to Azure 
slug: static-site-generator-with-python-azure
date: 02 Aug 2022 08:00
image: https://kjaymiller.azureedge.net/media/az%20deployment%20build.png
---

> TLDR: Connect your repo to Azure Static Web Apps and use GitHub Actions to build your site via Python.

Modern Static Sites (popularly referred to as [JAMstack Apps](https://jamstack.org)) provide a custom web experience for little to no cost.

I've been working on [my own static site generator](https://render-engine.readthedocs.io/en/latest/) for going on 5 years now. It's developed a lot over time, but one thing is consistent. It's modern python!

![output of my static site generator building files](https://kjaymiller.azureedge.net/media/render-engine-output.png)

Many folks have used tools like [github pages](https://pages.github.com), [Netlify](https://netlify.com) or [Vercel](https://vercel.com), since joining Microsoft, I wanted to learn more about how to make both static and dynamic sites using Python and [Azure](https://azure.microsoft.com/en-us/).

I first learned about Static Web Apps (SWA) in my first week when the team was [celebrating one year](https://techcommunity.microsoft.com/t5/apps-on-azure-blog/learn-azure-static-web-apps-in-30daysofswa/ba-p/3354021) of the product. By design, the plan was to serve web applications by mixing HTML and optionally dynamic content via Azure functions.

Python has fallen out of favor for building static web apps, but it is still possible to deploy a static web app. Sadly, you do have to do a little more than if you were going to use Javascript.

## Setup Azure Static Web Apps (The VS Code way)
You can setup Azure Static Web Apps with VS Code using the [Azure Static Web Apps Getting Started](https://docs.microsoft.com/en-us/azure/static-web-apps/getting-started?tabs=vanilla-javascript#install-azure-static-web-apps-extension). There provides a few options for web frameworks and the closest for you will be the vanilla JS route. We'll skip the first couple steps since we're not using the demo repo (or Javascript). I don't want to re-hash the tutorial; here is a quick recap:

1. Open your project's repo in VS Code
2. Install the Azure Extension and log in to your Azure account
3. Select the Azure Side bar menu in the _RESOURCES_ tab 
4. Select the create icon (plus sign)
5. In the prompt, choose _Create Static Web App_
6. Run through the wizard
   1. connecting your GitHub account
   2. creating a name for your project
   3. choose your preffered region

The next step is where things begin to differ.
1. **IMPORTANT** Selecting **CUSTOM** as the Deployment Method.  
2. Set your app location to "/" path of your project or wherever your Python code lives.
3. Set the output path to the location where your code will create HTML.

![gif of building out the steps in VS Code](https://kjaymiller.azureedge.net/media/NewSWAApp.gif)

## Getting your site up and running

Sadly, Azure Static Web Apps don't support running python based build commands easily, but according to the docs, we just need **ONE HTML** file in a folder to build a site. we can give it that file in a few different ways. Where you build your HTML will be up to you.

## Build in the image
Azure uses a system called [Oryx](https://github.com/Microsoft/Oryx). You don't need to know too much about how it works but it looks for specific files and chooses build specs based on them. If you have a `requirements.txt`, Oryx will know to use Python. [^1]

Using Oryx comes with a few compromises. Oryx uses a Python 3.8 build by default. You can update up to Python 3.9.7 by adding `PYTHON_VERSION: "3.9.7"` to the yaml file. Also, you will need to add your build steps to the  `PRE_BUILD_COMMAND`[^2]. You can create shell script or add the steps seperated with `&&`. 

```yaml
- name: Build And Deploy
        id: builddeploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN_MY_PROJECT }}
          repo_token: ${{ secrets.GITHUB_TOKEN }} # Used for Github integrations (i.e. PR comments)
          action: "upload"
          ###### Repository/Build Configurations - These values can be configured to match your app requirements. ######
          # For more information regarding Static Web App workflow configurations, please visit: https://aka.ms/swaworkflowconfig
          app_location: "/" # App source code path
          output_location: "OUTPUT_PATH" # Built app content directory - optional
        env:
          PYTHON_VERSION: 3.9.7
          PRE_BUILD_COMMAND: 'pip --upgrade pip && pip install -r requirements.txt && python routes.py' # This can be a shell script as well
```

### Build Before the Image
You can separate your build steps from the Azure image deployed, building it in Github Actions. 

To build your environment in GH Actions you'll need to add a block to your yaml file **BEFORE** the Azure `Build and Deploy` section. You'll need to include the `setup-python` action and specify the python version you would like to use. Use the major version of your python version so `3.10` and NOT `3.10.5`. For more information and options on this you can check out the [Setup-Python GH actions repo](https://github.com/actions/setup-python).

Next you'll need to add the run steps. Give this section a new name and enter the commands to run. 

```yaml
    run: az_build.sh # My run script is routes.py
```

For more than one command, use `|-` at the beginning which each command being on its own line.

I don't think there is much of a difference performance-wise. You're code is doing the same thing, just in a different place. Use this method to bypass Python version limits of Oryx (or separate concerns in your build).

![The build in GH Actions](https://kjaymiller.azureedge.net/media/Build%20in%20github%20actions.png)

### Build Before Pushing to Github
There is another way. Build your site locally and push its contents to GithHub.

You will need to manually run your build steps. The biggest advantages is complete control and you don't have to modify your yaml file.

The advantage of doing this is if you do granular changes, you don't have to rebuild the entire site.

## Viewing your Site
After you push your code to GitHub. You'll be able to see your site live. If you aren't sure of the URL, check the GitHub Actions Build and it will tell you in the build steps. 

![The Successful build with url](https://kjaymiller.azureedge.net/media/az%20deployment%20build.png)

You can also refresh the Azure Section of VS Code and it should be visible.

![The new SWA in VS Code](https://kjaymiller.azureedge.net/media/swa-output-vs-code.png)

Once it's running you can [add a custom domain](https://docs.microsoft.com/en-us/azure/static-web-apps/custom-domain) in the Azure Portal. 


[^1]: Sadly I don't think this works in Azure Static Web Apps using Pipenv or Poetry.

[^2]: You can add also add those steps to the `POST_BUILD_COMMAND`.