from django.http import HttpResponse
try:
    import uwsgi

    from django.core.management.commands import migrate
    from replays.management.commands import setup_constant_tables
    from thscoreboard import settings
    
    import bcrypt
    import os

    def deploy(request):
        if 'Deploy-Key' in request.headers and request.headers['Deploy-Key'] == settings.DEPLOY_KEY:
            os.system("git pull")

            migrate.Command().handle(
                database="default",
                skip_checks=False,
                verbosity=1,
                interactive=False,
                run_syncdb=False,
                app_label="",
                prune="",
                plan=""
            )

            setup_constant_tables.SetUpConstantTables()

            uwsgi.reload()
            return HttpResponse(content="<h1>Deployed!</h1>", status=200)
        else:
            return HttpResponse(content="<h1>Unauthorized!</h1>", status=403)
except ImportError:
    print("Could not import uwsgi module. Automatic deployment at /deploy unavailable")
    def deploy(request):
        return HttpResponse(content="<h1>Automatic deployment unavailable</h1>", status=501)

