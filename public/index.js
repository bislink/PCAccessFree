// public/index.js

// All cookies
	var all_cookies = document.cookie;
	
	// first cookie 
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(';');
	var pca_cookie = ca[0];
	var pca = pca_cookie.split('=', 2);
	
	//set cookie 
	if (pca_cookie != "") {
		//		
	}
	else { 
		document.cookie = "pcaccessfree=PCAccess Free; path=/; ";
	}
	
	
	var out = '';

	out += '<table>';
	
	var pcaDiv = document.getElementById('pcaccess-assistant');
	
	var host = window.location.host;            // with port
	var hostname = window.location.hostname;   // without port 
	var port = window.location.port;
	var pathname = window.location.pathname;
	var protocol = window.location.protocol;
		
	var path = new Array();
	path = pathname.split('/');
	 
	
// populate
	//
	out += '<tr> <td>Refresh</td><td><a href="' +protocol+ '//' +host+ '' +pathname+ '">This Page</a></td></tr>'; 
	//
	out += '<tr> <td>Protocol</td><td>' +protocol+ '</td></tr>';
	//host 
	//out += '<tr> <td>Host</td><td>' +host+ '</td></tr>';
	//
	out += '<tr> <td>Hostname</td><td>' +hostname+ '</td></tr>';
	// port 
	out += '<tr> <td>Port</td><td>' +port+ '</td></tr>';
	// pathname 
	out += '<tr> <td>PCAccess Dir.</td><td>' +path[1]+ '</td></tr>';
	
// cookie 
	//
	//out += '<tr> <td>PCA Cookie Name</td><td>' +pca[0]+ '</td></tr>';
	//
	//out += '<tr> <td>PCA Cookie Value</td><td>' +pca[1]+ '</td></tr>';
	//
	
	
	//
	//out += '<tr> <td>All Cookies</td><td>' +cookie+ '</td></tr>';
	
	
	
	out += '</table>';
	
// Final output
	// pcaccess-assistant
	pcaDiv.innerHTML = out;
	// rights
	document.getElementById('copy-rights').innerHTML = '&amp; ' +hostname; 
	//
	document.getElementById('sponsors').innerHTML = sponsors();

	
