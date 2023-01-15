from pyngrok import ngrok
from github import Github
import os


JENKINS_HOST = "127.0.0.1:8080"
REPO_NAME = "coding_practice"
EVENTS = ["push", "pull_request"]
ENDPOINT = "github-webhook"
TOKEN = os.getenv("GITHUB_TOKEN")


if __name__ == "__main__":
    ngrok_process = ngrok.get_ngrok_process()
    http_tunnel: ngrok.NgrokTunnel | None = None

    try:
        # Block until CTRL-C or some other terminating event
        http_tunnel = ngrok.connect(JENKINS_HOST)

        print(f"Server is listening on {http_tunnel.public_url}")

        g = Github(TOKEN)

        config = {
            "url": "{host}/{endpoint}".format(
                host=http_tunnel.public_url,
                endpoint=ENDPOINT
            ),
        }

        repo = g.get_user().get_repo(REPO_NAME)
        repo.create_hook("web", config, EVENTS, active=True)

        ngrok_process.proc.wait()
    except KeyboardInterrupt:
        print("Shutting down server.")

        ngrok.kill()
