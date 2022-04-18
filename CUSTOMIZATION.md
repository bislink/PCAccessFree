# PC Access Free - Optional Customizations

## How to enable SSL for your IIS default website?

## Import SSL Certificate to IIS

First, if you have your own domain name, setup a subdomian called `pca.YOURNAME.tld` and request SSL for it. Ask your hosting provider.

If not, request SSL certificate for `YOURNAME.bislinks.com` from https://pcafree.bislinks.com

### Assuming, you have downloaded `YOURNAME.TLD.pfx` file to your computer, e.g., to `C:/Users/USER/Documents` from your hosting provider.

```
Open IIS as Administrator
Under Connections, Click on your main IIS Server Connection, usually your computer name
In the middle pane, double click "Server Certificates"
Under Actions, click 'import'
In the 'import certificate' dialogue, under 'certificate file .pfx,' select location `c:/Users/USERNAME/Documents`
and select .pfx file you just downloaded
```

### Video

https://youtu.be/QMqcQB_aGDg



## Add/Enable HTTPS

```
Open IIS as Administrator
Under connections, selet your site
Under Actions, click bindings
Under Actions, click bindings
Under Site Bindings, click add
Under Type, select https
Under IP Address, Select "All Unassigned"
Under Port, leave it as `443` or assign a custom port above 10000, e.g., 21202 or 20443 or 30443 or 40443
Under SSL Certificates, Select `YOURNAME.TLD`
Check "Disalbe HTTP/2" in order to disable http2
Clcik OK to save
Click close to close Site Bindings.

```


## Disable http2 in IIS

### For SSL sites only

```
Open IIS as Administrator
Under connections, selet your site
Under Actions, click bindings
Under Site Bindings, Select https and click edit
Check/enable the "Disable HTTP/2" option
```

### Video

https://www.youtube.com/watch?v=EwIRbf-9emY
