from django.http import HttpResponse
try:
    import uwsgi

    from django.contrib.staticfiles.management.commands import collectstatic
    from sass_processor.management.commands import compilescss
    from django.core.management.commands import migrate

    from django.core.exceptions import ObjectDoesNotExist
    from django.contrib.auth.hashers import check_password
    from users.models import User
    from replays.management.commands import setup_constant_tables
    
    import base64
    import os

    def do_deploy():
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

        compilescss.Command().handle(
            verbosity=1,
            delete_files=False,
            use_storage=False,
            sass_precision=True
        )

        collectstatic.Command().handle(
            interactive=False,
            verbosity=1,
            link=False,
            clear=True,
            dry_run=False,
            ignore_patterns=[],
            use_default_ignore_patterns=False,
            post_process=False
        )

        uwsgi.reload()

    def deploy(request):
        if "Authorization" in request.headers:
            auth = request.headers["Authorization"].split(' ')
            if len(auth) == 2 and auth[0] == "Basic":
                creds = base64.b64decode(auth[1]).decode().split(':')
                try:
                    user = User.objects.get(username=creds[0])
                    if check_password(creds[1], user.password) and user.is_superuser:
                        do_deploy()
                        return HttpResponse(status=200, content="Success!!!")
                except ObjectDoesNotExist:
                    response = HttpResponse(status=401, content=f"Failed to authenticate user {creds[0]}")
                    response.headers["WWW-Authenticate"] = "Basic"
                    return response
        response = HttpResponse(status=401)
        response.headers["WWW-Authenticate"] = "Basic"
        return response

except ImportError:
    print("Could not import uwsgi module. Automatic deployment at /deploy unavailable")

    def deploy(request):
        return HttpResponse(content="<h1>Automatic deployment unavailable</h1>", status=501)
