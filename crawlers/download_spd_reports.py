import os
os.system('rm /tmp/cookiefile')
#os.system('rm /home/ubuntu/redactvideodotorg/static/police_reports/*.pdf;')
cmd = "curl -s --cookie-jar /tmp/cookiefile 'https://web1.seattle.gov/doit/sso/login.aspx?ReturnUrl=%2fpolice%2frecords%2fPoliceReports%2fDefault.aspx&IsReturnUrlSSL=false'  -H 'Origin: https://web1.seattle.gov' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8,es;q=0.6' -H 'Upgradensecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Referer: https://web1.seattle.gov/doit/sso/login.aspx?ReturnUrl=%2fpolice%2frecords%2fPoliceReports%2fDefault.aspx&IsReturnUrlSSL=false' -H 'Connection: keep-alive' --data '__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=NsmJy86fbmP27qHvJWxwYF6N1i2p1PLthlfLizrcNe2z83QynAtUqJi%2FhOv6dHrUbn3AQupG%2FBmy3uPD0qaf2KvySkldyOnjul6hjtebOnaQkk4zif5dff%2F3ltrVeHHNbutosFiqBe%2FAHqgGpwOSnWTVxsHNtDY%2BP9Uzv0J7PaCoHedzkLFYr%2BQsEmI2uJuDLVuvzNRbmkNZ%2Fvcb9loRTIsgbZ3xKiKP74Bws0ecIquRQ8jdVBpMfxOgxM%2Fz45jlFb%2FaDXJvGYiWZT361Z6TCiWDTECtSKMmbY%2FupnTUmvXH6XxKaCN%2Fph0ur%2BAob%2FE6t4q6wqMj2emQeVK8AZnMrru7U6LdlsWTZ3tks0onPrm%2FvM79af9B%2BaspjKDFxNfrOWWOoNnmCktFYaFNQjbWxwxygv006%2F%2FIBCGGhr085%2FtYuhIFOSMCi%2BikeA8B6qK6MvpdugdzruURb98bkyIVwFgLKyXJh5ibXaD8s%2B8z557BHoO4jHdYA01gLZ7tZ4i9%2F%2Bq0MPbezOvkVBXvbWA9PpUnNnipW6U3y4A6jUoBU0vLriOhMWapczgaOdN5zJz9P13j0Lr9IBylfa9qhBX6RGPK0qpc%2B7lbCF0uarJnJtqAbWKlLpiIP2gm8JIQS9C2fWWP37fpdxJ4Lvg9TLQbtfHkKpN%2Fj3kSf7ry7BCx8isliIBVG1gvhcomhMfmoQnJMf9Uv%2FHUjBSRdItHdFDrp2G8JiQtgE3Pzs5ANlvvjSfW%2BGEl7Br2oQMROI8SpMKIW6%2FagUCINfl7XTs3tSLnOFfDdMm3p8M2pgiseYtFMzLnrQrfn%2F2MT198TFed%2FscfRv41B%2FOoWWKgIQImrbF9VnIwOO%2FV%2F9utw59OiB%2BNH9jGj4Or02NkY80oBWn3Zd6AMgcnbZUKkIRJ0nCxFMkYrAPVIIg%3D&__VIEWSTATEGENERATOR=022333B8&__SCROLLPOSITIONX=0&__SCROLLPOSITIONY=0&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION=xHm1pbRIbr4HH19mWApVlYWHYbk5GK8axuV0DB2xtA3WMjZMu9oMCteqlnprOABJBSLTIPacal%2BWILk8m8u5UySeNHKKnZKf25MiYaK%2FV2zstuph&ctl00%24MainContentPlaceHolder%24AppLogin%24Email=timothy.clemans%40gmail.com&ctl00%24MainContentPlaceHolder%24AppLogin%24Password=ssgmssgm2&ctl00%24MainContentPlaceHolder%24AppLogin%24LoginButton=Sign+In' -k --compressed"
print cmd 
os.system("curl -s --cookie-jar /tmp/cookiefile 'https://web1.seattle.gov/doit/sso/login.aspx?ReturnUrl=%2fpolice%2frecords%2fPoliceReports%2fDefault.aspx&IsReturnUrlSSL=false'  -H 'Origin: https://web1.seattle.gov' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8,es;q=0.6' -H 'Upgradensecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Referer: https://web1.seattle.gov/doit/sso/login.aspx?ReturnUrl=%2fpolice%2frecords%2fPoliceReports%2fDefault.aspx&IsReturnUrlSSL=false' -H 'Connection: keep-alive' --data '__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=NsmJy86fbmP27qHvJWxwYF6N1i2p1PLthlfLizrcNe2z83QynAtUqJi%2FhOv6dHrUbn3AQupG%2FBmy3uPD0qaf2KvySkldyOnjul6hjtebOnaQkk4zif5dff%2F3ltrVeHHNbutosFiqBe%2FAHqgGpwOSnWTVxsHNtDY%2BP9Uzv0J7PaCoHedzkLFYr%2BQsEmI2uJuDLVuvzNRbmkNZ%2Fvcb9loRTIsgbZ3xKiKP74Bws0ecIquRQ8jdVBpMfxOgxM%2Fz45jlFb%2FaDXJvGYiWZT361Z6TCiWDTECtSKMmbY%2FupnTUmvXH6XxKaCN%2Fph0ur%2BAob%2FE6t4q6wqMj2emQeVK8AZnMrru7U6LdlsWTZ3tks0onPrm%2FvM79af9B%2BaspjKDFxNfrOWWOoNnmCktFYaFNQjbWxwxygv006%2F%2FIBCGGhr085%2FtYuhIFOSMCi%2BikeA8B6qK6MvpdugdzruURb98bkyIVwFgLKyXJh5ibXaD8s%2B8z557BHoO4jHdYA01gLZ7tZ4i9%2F%2Bq0MPbezOvkVBXvbWA9PpUnNnipW6U3y4A6jUoBU0vLriOhMWapczgaOdN5zJz9P13j0Lr9IBylfa9qhBX6RGPK0qpc%2B7lbCF0uarJnJtqAbWKlLpiIP2gm8JIQS9C2fWWP37fpdxJ4Lvg9TLQbtfHkKpN%2Fj3kSf7ry7BCx8isliIBVG1gvhcomhMfmoQnJMf9Uv%2FHUjBSRdItHdFDrp2G8JiQtgE3Pzs5ANlvvjSfW%2BGEl7Br2oQMROI8SpMKIW6%2FagUCINfl7XTs3tSLnOFfDdMm3p8M2pgiseYtFMzLnrQrfn%2F2MT198TFed%2FscfRv41B%2FOoWWKgIQImrbF9VnIwOO%2FV%2F9utw59OiB%2BNH9jGj4Or02NkY80oBWn3Zd6AMgcnbZUKkIRJ0nCxFMkYrAPVIIg%3D&__VIEWSTATEGENERATOR=022333B8&__SCROLLPOSITIONX=0&__SCROLLPOSITIONY=0&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION=xHm1pbRIbr4HH19mWApVlYWHYbk5GK8axuV0DB2xtA3WMjZMu9oMCteqlnprOABJBSLTIPacal%2BWILk8m8u5UySeNHKKnZKf25MiYaK%2FV2zstuph&ctl00%24MainContentPlaceHolder%24AppLogin%24Email=timothy.clemans%40gmail.com&ctl00%24MainContentPlaceHolder%24AppLogin%24Password=ssgmssgm2&ctl00%24MainContentPlaceHolder%24AppLogin%24LoginButton=Sign+In' -k --compressed")

for case_type in ['BURGLARY', 'ROBBERY', 'ASSUALT']:
    results = os.popen(r"curl -s --cookie /tmp/cookiefile 'http://web1.seattle.gov/police/records/PoliceReports/Search.aspx' -H 'Origin: http://web1.seattle.gov' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8,es;q=0.6' -H 'Upgradensecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Referer: http://web1.seattle.gov/police/records/PoliceReports/Search.aspx' -H 'Connection: keep-alive' --data '__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=Ag4ng%2F6Z4lQjULA6irpN121BlXx%2B0XySml99fFaojCUkXe3azriO7f%2BGLmWFkULfenTRNjdLAzz5JNb9yLhvf6Y90UuFTy7QdDfyML%2F27zDOMgfOG6ejQzCuK4JgtQ6EQ%2FTedg9ItquqOYgEYHi%2FA82eGzPnSXRjKCeurg%2F%2Fg091Xr22BQeNFDblHk1GUrJjyVwK8X0pssy9hvqW%2BBiARRnam6JT4%2B3DDART6gi6Pg9JGjVD4y1Rsprx0OaqRK1VB3Yxwje32tDpNVfCrpvPH9nLVrGaOO2rRdxTwri1Lwv7GTQGycvGf57z%2FErwwjKlEhZLk9iQ296RXZbipEhsPLOcfesCtD9GoiPTbRw45GmtQrFqow1Mm4Sj0vxGp2jSuDkiH50QVekr%2BB290TObVPNn%2BaS9lArvhgXLSY9tyD2a6pm0QwXKOPWJqBGUBWmgj4iB7voPSAr9KWVnJT998kZqWvPIlRrZl7YzPjkGogTPAPI2JNsCCnOMOis5FA%2B5IXqfo1msEQ%2B1%2Blv5njSRZNYvuWFiY3hyykn%2BvIm3hG6BwweC8Pso3et426dT29jInWs%2FRsqDSzXyCYPIezCt2zenf6kI%2F1DQZTgv9RzJIBE0pnCyz6E0Gs6B1t7rip6%2FY%2Fwl9nsvYVJpZPaqflHcX89FABYBXziLcX56aOQTo7H0zedBVEZGiAgFeG0tLVFwsusmORJVT7YvzWug1uIllcnHaF6w176sUG5BCGEFZigl53lgc%2B9R3I5xSFJLzhvcVCixcQqraBjDDXvXRJt6H3UUhQULzx%2Bu6ZfHVIEghCjXD0XWwQlPERY9ATGH7VguZf0Lzzug2yCdXqBoKjulzhXP8UTQW3AO33LJxf0q%2BajaApDYrHFLApyVkEYmDpttp7M1NBcGvyR0v6WPJrIs8MMtoK21gKF2t459RvxPu5XbHXyGPX2ublgB1gNOaQnyxe0ZJEitt59Hy6VjfW7zG8W%2BS0bWaFnH8y6q16uO%2F23tSOM4tyYt4vBGQoXlbzgzLNxhzA8cc%2FYZbY5r1i%2BGtJixJ%2Fv4%2BkaDijMMofblx%2BDl4pA%2Br6KIKSNPs7%2Fc6nipITxuWcslo9twB0lbqWs3CMlFY50dRAQJXN2vj1C8hHW04yE4qUhsIHPzGfk4H1e%2BSUok82EcXrXmWTB7Zq6zi48batZUom06tL%2BrKx5529TuuPhzKdUMaXzx8N2yDE3DMiN2CFUo5od%2FLuEUDHyJxMvUR9YRuUpWEScy1ALDG%2B3SvUAlEyBNc%2FymvSGUqN7Wd%2Fya5gNK7hVYcymTmhPt4YaGBrWyFu%2BolRDIDeodPkkhcm4NaPNcMehalEDc%2BsK9IkisXpNlCmTnOy9pbOY5KxmXM4OSObpD7epQ4JpZO%2FvzUBk4vHhGRSXByZhA9xKHI%2Bzf7nCwaYTCj0%2BqoHmXjZM2SR3XKpPnAvWYLxFJ9xqkSTZvAHQVU2cb2sBi7gXJNm%2FYGVMynUCn71A1ifYZtCKprhSVPuwW%2Fbagsa%2FTpEZXgVuanVkUI0lzKTLWyILTtZg3W9HGMjWigtLBwq1CoR2hYOO3WEfe52YhvECYmlKN%2FpMST%2BBHuuT2ahcKW3kMjkH3EUQ7mM0UYByiDPRAn5FA%2FN5FqmD4v%2FxxclzZw6eBq33MdXk7%2B4gW8M2XLzPqdN4MTUG3F53bl696db4ReAxwdKkuzGnLKpsPXD8C%2Bjt%2Bcacg7SlyRdBdRGL8L%2F6vX9pVkPxsjMT4ZCtrTjYgDNsjS6OnzcGtliF01JP996SMNY0wapkjzhnvl7FD31X85yPc4%2Bko9d%2F0QKUl3s3l2HsCZu0ERg8JxlkStZVK%2FkTeJ63MtmRfwW8CqTi11WoIqdedT2nWW4M9EcGAiQmsbbbJepcT4c5IsHiHg2iU6I1ta6yOzVbuQ1fWeNE0PRIZOm1MY%2FsgiZW8vV7res%2BbwpYIzUvi3DN3DxHuPmA0oBaHT9eliysu90YHY3SQpfQdhROZiIkwg5gZSQlVFx2iyclKx%2BuBSG0mAbuIV5kkF%2BSTVCsJ&__VIEWSTATEGENERATOR=32F1E5CB&__EVENTVALIDATION=4KHtDnaEVGY8JYnmzLlfv1eXqc4jY6cBR%2Fg0S5uEmZa%2Bjn6omhZinluCV4dOKv%2BZ1rx%2FoP9bxDfb38yxfgpDfFBC8mwcNw1rvPRrY5hW4tahrWqeHVrfWf6VqCA%2BbfxIxzQFOmH44%2BFoGmOZ%2BK9Lg0fCAyOrGW6zER0CYcY4ErE2rQc3I9614xTz11yw56if0cMVKbAmZCwffJCB3uD%2Bv8ktzOPCH2LYsIgPQzFmmDyj6S2oG5VV5TmHDfjBzDjyn5xXskml9x3kVrYtMS%2FArekES8Uil5lXj1jl1n0NuP4QCnOosbIj%2B%2B8P2O1V7BhPt9PLoLJxx8WhsdulgPmWVJ6%2BMTxUoFDop2sS96E4Khyvkewgb7hd220Lx8Djqy1LQiKTRiNY7P5GFzQmhNDm9BC%2BEbSCCSNFm8G8PRA1%2BftMrRP5P6M6tHjHVlidr5bf7grWqc2FEJqvo07AUTP%2FYAHc%2FKJtVvmM4DhJLhdCRy5y1YZdwZndOxKaEbt8ONM%2F4oGOAhd2bbnXVHIs&q=&ctl00%24MainContentPlaceHolder%24OffenseTypeDropDownList="+case_type+"&ctl00%24MainContentPlaceHolder%24DateRange1TextBox=04%2F01%2F2014&ctl00%24MainContentPlaceHolder%24DateRange2TextBox=11%2F09%2F2015&ctl00%24MainContentPlaceHolder%24SearchButton=Search' --compressed -k").read()
    print len(results)
    import re
    base_url = 'http://web1.seattle.gov/police/records/PoliceReports/'
    links = re.findall('<a class="med_blue" href=\'(?P<url>PoliceReport.ashx\?go=\d+)\' target="_blank">.*\*</a', results)
    for link in links:
        os.system('mkdir /home/ubuntu/spd_police_reports/')
        if link[link.find('=')+1:]+".pdf" in os.listdir('/home/ubuntu/spd_police_reports/'):
            #print  link[link.find('=')+1:]+".pdf", os.listdir('.')
            continue
        cmd = "curl -s --cookie /tmp/cookiefile '"+base_url+link+"' -k > /home/ubuntu/spd_police_reports/"+link[link.find('=')+1:]+".pdf"
        print cmd
        results = os.popen(cmd).read()
        print results