# Next Steps

Your archive site has been scaffolded with a single default archive.

## Adding More Archives

To set up multiple archives (e.g., production, staging):

    regis archive configure --add "Production:static/archive/prod" -o static/archives.json
    regis archive configure --add "Staging:static/archive/staging" -o static/archives.json

Then add reports to each:

    regis analyze <IMAGE> --archive static/archive/prod
    regis analyze <IMAGE> --archive static/archive/staging

List configured archives:

    regis archive configure --list static/archives.json

The dashboard will automatically show archive tabs when archives.json is present.
