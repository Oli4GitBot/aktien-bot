ython3 sp500_screener.py
  shell: /usr/bin/bash -e {0}
  env:
    pythonLocation: /opt/hostedtoolcache/Python/3.11.15/x64
    PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib/pkgconfig
    Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
    Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
    Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
    LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
    TELEGRAM_BOT_TOKEN: 
    TELEGRAM_CHAT_ID: 
    GITHUB_EVENT_NAME: workflow_dispatch
2026-06-17 17:29:59,275 [INFO] Lade S&P-500-Liste von Wikipedia...
Error: -17 17:29:59,507 [ERROR] Konnte S&P-500-Liste nicht laden: [Errno 2] No such file or directory: <!DOCTYPE html>
<html class="client-nojs vector-feature-language-in-header-enabled vector-feature-language-in-main-menu-disabled vector-feature-language-in-main-page-header-disabled vector-feature-page-tools-pinned-disabled vector-feature-toc-pinned-clientpref-1 vector-feature-main-menu-pinned-disabled vector-feature-limited-width-clientpref-1 vector-feature-limited-width-content-enabled vector-feature-custom-font-size-clientpref-1 vector-feature-appearance-pinned-clientpref-1 skin-theme-clientpref-day vector-sticky-header-enabled vector-toc-available skin-thumbsize-clientpref-standard" lang="en" dir="ltr">
<head>
<meta charset="UTF-8">
<title>List of S&amp;P 500 companies - Wikipedia</title>
<script>(function(){var className="client-js vector-feature-language-in-header-enabled vector-feature-language-in-main-menu-disabled vector-feature-language-in-main-page-header-disabled vector-feature-page-tools-pinned-disabled vector-feature-toc-pinned-clientpref-1 vector-feature-main-menu-pinned-disabled vector-feature-limited-width-clientpref-1 vector-feature-limited-width-content-enabled vector-feature-custom-font-size-clientpref-1 vector-feature-appearance-pinned-clientpref-1 skin-theme-clientpref-day vector-sticky-header-enabled vector-toc-available skin-thumbsize-clientpref-standard";var cookie=document.cookie.match(/(?:^|; )enwikimwclientpreferences=([^;]+)/);if(cookie){cookie[1].split('%2C').forEach(function(pref){className=className.replace(new RegExp('(^| )'+pref.replace(/-clientpref-\w+$|[^\w-]+/g,'')+'-clientpref-\\w+( |$)'),'$1'+pref+'$2');});}document.documentElement.className=className;}());RLCONF={"wgBreakFrames":false,"wgSeparatorTransformTable":["",""],"wgDigitTransformTable":["",""],"wgDefaultDateFormat":"dmy","wgMonthNames":["","January","February","March","April","May","June","July","August","September","October","November","December"],"wgRequestId":"a738e763-0b8b-420f-9a59-3871ef7379b1","wgCanonicalNamespace":"","wgCanonicalSpecialPageName":false,"wgNamespaceNumber":0,"wgPageName":"List_of_S\u0026P_500_companies","wgTitle":"List of S\u0026P 500 companies","wgCurRevisionId":1359811933,"wgRevisionId":1359811933,"wgArticleId":2676045,"wgIsArticle":true,"wgIsRedirect":false,"wgAction":"view","wgUserName":null,"wgUserGroups":["*"],"wgCategories":["All articles with dead external links","Articles with dead external links from August 2023","Articles with permanently dead external links","CS1 maint: numeric names: authors list","Articles with dead external links from November 2019","Articles with dead external links from May 2026","Articles with short description","Short description is different from Wikidata","Use American English from April 2026","All Wikipedia articles written in American English","Use mdy dates from April 2026","All articles with unsourced statements","Articles with unsourced statements from April 2025","S\u0026P Dow Jones Indices","Lists of companies"],"wgPageViewLanguage":"en","wgPageContentLanguage":"en","wgPageContentModel":"wikitext","wgRelevantPageName":"List_of_S\u0026P_500_companies","wgRelevantArticleId":2676045,"wgTempUserName":null,"wgIsProbablyEditable":true,"wgRelevantPageIsProbablyEditable":true,"wgRestrictionEdit":[],"wgRestrictionMove":[],"wgNoticeProject":"wikipedia","wgFlaggedRevsParams":{"tags":{"status":{"levels":1}}},"wgConfirmEditCaptchaNeededForGenericEdit":"hcaptcha","wgConfirmEditForceShowCaptcha":false,"wgConfirmEditHCaptchaSiteKey":"5d0c670e-a5f4-4258-ad16-1f42792c9c62","wgMediaViewerOnClick":true,"wgMediaViewerEnabledByDefault":true,"wgMediaViewerMobileBeta":false,"wgPopupsFlags":0,"wgVisualEditor":{"pageLanguageCode":"en","pageLanguageDir":"ltr","pageVariantFallbacks":"en"},"wgMFDisplayWikibaseDescriptions":{"search":true,"watchlist":true,"tagline":false,"nearby":true},"wgWMESchemaEditAttemptStepOversample":false,"wgWMEPageLength":200000,"wgTestKitchenUserExperiments":{"overrides":[],"enrolled":[],"assigned":[],"subject_ids":[]},"wgEditSubmitButtonLabelPublish":true,"wgVisualEditorPageIsDisambiguation":false,"wgULSPosition":"interlanguage","wgULSisCompactLinksEnabled":false,"wgVector2022LanguageInHeader":true,"wgULSisLanguageSelectorEmpty":false,"wgULSLanguageSelectorV2Enabled":false,"wgWikibaseItemId":"Q6596115","wgCheckUserClientHintsHeadersJsApi":["brands","architecture","bitness","fullVersionList","mobile","model","platform","platformVersion"],"wgPersonalDashboardMenuVisible":false};
RLSTATE={"ext.globalCssJs.user.styles":"ready","site.styles":"ready","user.styles":"ready","ext.globalCssJs.user":"ready","user":"ready","user.options":"loading","ext.wikimediamessages.styles":"ready","ext.cite.styles":"ready","skins.vector.search.codex.styles":"ready","skins.vector.styles":"ready","skins.vector.icons":"ready","jquery.tablesorter.styles":"ready","jquery.makeCollapsible.styles":"ready","ext.visualEditor.desktopArticleTarget.noscript":"ready","ext.uls.interlanguage":"ready","wikibase.client.init":"ready"};RLPAGEMODULES=["ext.parsermigration.survey","ext.cite.ux-enhancements","mediawiki.page.media","site","mediawiki.page.ready","jquery.tablesorter","jquery.makeCollapsible","mediawiki.toc","skins.vector.js","ext.centralNotice.geoIP","ext.centralNotice.startUp","ext.gadget.ReferenceTooltips","ext.gadget.switcher","ext.urlShortener.toolbar","ext.centralauth.centralautologin","ext.testKitchen","mmv.bootstrap","ext.popups","ext.visualEditor.desktopArticleTarget.init","ext.echo.centralauth","ext.eventLogging","ext.wikimediaEvents","ext.navigationTiming","ext.uls.interface","ext.cx.eventlogging.campaigns","ext.cx.uls.quick.actions","wikibase.client.vector-2022","wikibase.databox.fromWikidata","ext.checkUser.clientHints","ext.quicksurveys.init"];</script>
<script>(RLQ=window.RLQ||[]).push(function(){mw.loader.impl(function(){return["user.options@12s5i",function($,jQuery,require,module){mw.user.tokens.set({"patrolToken":"+\\","watchToken":"+\\","csrfToken":"+\\"});
}];});});</script>
<link rel="stylesheet" href="/w/load.php?lang=en&amp;modules=ext.cite.styles%7Cext.uls.interlanguage%7Cext.visualEditor.desktopArticleTarget.noscript%7Cext.wikimediamessages.styles%7Cjquery.makeCollapsible.styles%7Cjquery.tablesorter.styles%7Cskins.vector.icons%2Cstyles%7Cskins.vector.search.codex.styles%7Cwikibase.client.init&amp;only=styles&amp;skin=vector-2022">
<script async="" src="/w/load.php?lang=en&amp;modules=startup&amp;only=scripts&amp;raw=1&amp;skin=vector-2022"></script>
<meta name="ResourceLoaderDynamicStyles" content="">
<link rel="stylesheet" href="/w/load.php?lang=en&amp;modules=site.styles&amp;only=styles&amp;skin=vector-2022">
<meta name="generator" content="MediaWiki 1.47.0-wmf.6">
<meta name="referrer" content="origin">
<meta name="referrer" content="origin-when-cross-origin">
<meta name="robots" content="max-image-preview:standard">
<meta name="format-detection" content="telephone=no">
<meta property="og:image" content="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/S%26P_500_Headquarters.svg/1280px-S%26P_500_Headquarters.svg.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="645">
<meta name="viewport" content="width=1120">
<meta property="og:title" content="List of S&amp;P 500 companies - Wikipedia">
<meta property="og:type" content="website">
<link rel="preconnect" href="//upload.wikimedia.org">
<link rel="alternate" type="application/x-wiki" title="Edit this page" href="/w/index.php?title=List_of_S%26P_500_companies&amp;action=edit">
<link rel="apple-touch-icon" href="/static/apple-touch/wikipedia.png">
<link rel="icon" href="/static/favicon/wikipedia.ico">
<link rel="search" type="application/opensearchdescription+xml" href="/w/rest.php/v1/search" title="Wikipedia (en)">
<link rel="EditURI" type="application/rsd+xml" href="//en.wikipedia.org/w/api.php?action=rsd">
<link rel="canonical" href="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies">
<link rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/deed.en">
<link rel="alternate" type="application/atom+xml" title="Wikipedia Atom feed" href="/w/index.php?title=Special:RecentChanges&amp;feed=atom">
<link rel="dns-prefetch" href="//meta.wikimedia.org" />
<link rel="dns-prefetch" href="auth.wikimedia.org">
<td><a href="/wiki/Fairfield,_Ohio" title="Fairfield, Ohio">Fairfield, Ohio</a></td>
<td>1997-12-18</td>
<td>0000020286</td>
<td>1950
</td></tr>
<tr>
<td><a rel="nofollow" class="external text" href="https://www.nasdaq.com/market-activity/stocks/ctas">CTAS</a>
</td>
<td><a href="/wiki/Cintas" title="Cintas">Cintas</a></td>
<td>Industrials</td>
<td>Diversified Support Services</td>
<td><a href="/wiki/Mason,_Ohio" title="Mason, Ohio">Mason, Ohio</a></td>
<td>2001-03-01</td>
<td>0000723254</td>
<td>1929
</td></tr>
<tr>
<td><a rel="nofollow" class="external text" href="https://www.nasdaq.com/market-activity/stocks/csco">CSCO</a>
</td>
<td><a href="/wiki/Cisco" title="Cisco">Cisco</a></td>
<td>Information Technology</td>
<td>Communications Equipment</td>
<td><a href="/wiki/San_Jose,_California" title="San Jose, California">San Jose, California</a></td>
<td>1993-12-01</td>
<td>0000858877</td>
<td>1984
</td></tr>
<tr>
<td><a rel="nofollow" class="external text" href="https://www.nyse.com/quote/XNYS:C">C</a>
</td>
<td><a href="/wiki/Citigroup" title="Citigroup">Citigroup</a></td>
<td>Financials</td>
<td>Diversified Banks</td>
<td><a href="/wiki/New_York_City" title="New York City">New York City</a>, New York</td>
<td>1988-05-31</td>
<td>0000831001</td>
<td>1998
</td></tr>
<tr>
<td><a rel="nofollow" class="external text" href="https://www.nyse.com/quote/XNYS:CFG">CFG</a>
</td>
<td><a href="/wiki/Citizens_Financial_Group" title="Citizens Financial Group">Citizens Financial Group</a></td>
<td>Financials</td>
<td>Regional Banks</td>
<td><a href="/wiki/Providence,_Rhode_Island" title="Providence, Rhode Island">Providence, Rhode Island</a></td>
<td>2016-01-29</td>
<td>0000759944</td>
<td>1828
</td></tr>
<tr>
<td><a rel="nofollow" class="external text" href="https://www.nyse.com/quote/XNYS:CLX">CLX</a>
</td>
<td><a href="/wiki/Clorox" title="Clorox">Clorox</a></td>
<td>Consumer Staples</td>
<td>Household Products</td>
<td><a href="/wiki/Oakland,_California" title="Oakland, California">Oakland, California</a></td>
<td>1969-03-31</td>
<td>0000021076</td>
<td>1913
</td></tr>
<tr>
<td><a rel="nofollow" class="external text" href="https://www.nasdaq.com/market-activity/stocks/cme">CME</a>
</td>
<td><a href="/wiki/CME_Group" title="CME Group">CME Group</a></td>
<td>Financials</td>
<td>Financial Exchanges &amp; Data</td>
<td><a href="/wiki/Chicago" title="Chicago">Chicago</a>, Illinois</td>
<td>2006-08-11</td>
<td>0001156375</td>
<td>1848
</td></tr>
<tr>
<td><a rel="nofollow" class="external text" href="https://www.nyse.com/quote/XNYS:CMS">CMS</a>
</td>
<td><a href="/wiki/CMS_Energy" title="CMS Energy">CMS Energy</a></td>
<td>Utilities</td>
<td>Multi-Utilities</td>
<td><a href="/wiki/Jackson,_Michigan" title="Jackson, Michigan">Jackson, Michigan</a></td>
<td>1957-03-04</td>
