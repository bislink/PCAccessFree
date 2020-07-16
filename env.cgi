#!/usr/bin/perl

use strict;


my $out = '';

	$out .= qq{<table class="table table-responsive table-striped table-compact">};
	if (%ENV) {

		for (keys %ENV) {
			$out .= qq{<tr> <td>$_</td> <td>$ENV{"$_"}</td> </tr>\n};
		}
		$out .= qq{</table>};
		
    }

print qq{Content-Type: text/html\n\n};
print qq{<!doctype html>
	<html lang="en">
	<head>
	
		<title>Environment - PC-Access Free</title>
	
		<meta charset="utf-8">
		<meta name="theme-color" content="black">
		<meta name="keywords" content="windows xp, windows 7, windows 8.1, windows 10, windows server 2012, file manager, blogs, hosted by a1z.us, pc access free">
		<meta name="description" content="Windows file Manager - PC Access Free">
		<meta name="viewport" content="width=device-width, initial-scale=1">
	
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" crossorigin="anonymous">
	
		<link rel="stylesheet" href="index.css">
	
		<link rel="manifest" href="manifest.json">
	
	</head>
	
	<body>

	<main>
};
print qq{$out};
print qq{
	</main>
};

