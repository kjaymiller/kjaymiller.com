Found 3 accessibility violations:
Rule Violated:
landmark-one-main - Ensures the document has a main landmark
	URL: https://dequeuniversity.com/rules/axe/4.4/landmark-one-main?application=axeAPI
	Impact Level: moderate
	Tags: ['cat.semantics', 'best-practice']
	Elements Affected:


	1)	Target: html
		Snippet: <html lang="en">
		Messages:
		* Document does not have a main landmark
Rule Violated:
link-name - Ensures links have discernible text
	URL: https://dequeuniversity.com/rules/axe/4.4/link-name?application=axeAPI
	Impact Level: serious
	Tags: ['cat.name-role-value', 'wcag2a', 'wcag412', 'wcag244', 'section508', 'section508.22.a', 'ACT']
	Elements Affected:


	1)	Target: .bg-gradient-to-br > .p-1:nth-child(3)
		Snippet: <a class="p-1" href="https://www.youtube.com/channel/UCjoJU65IbXkKXsNqydro05Q/">    <i class="text-red-700 text-2xl m-1 fa-brands fa-youtube"></i></a>
		Messages:
		* Element does not have text that is visible to screen readers
		* aria-label attribute does not exist or is empty
		* aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
		* Element has no title attribute
		* Element is in tab order and does not have accessible text

	2)	Target: .bg-gradient-to-br > .rounded-xl.opacity-50[href$="kjaymiller"]:nth-child(4)
		Snippet: <a class="rounded-xl opacity-50 p-1 hover:opacity-100" href="https://twitter.com/kjaymiller">    <i class=" text-blue-500 m-1 text-2xl fa-brands fa-twitter-square"></i></a>
		Messages:
		* Element does not have text that is visible to screen readers
		* aria-label attribute does not exist or is empty
		* aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
		* Element has no title attribute
		* Element is in tab order and does not have accessible text

	3)	Target: .rounded-xl.opacity-50.p-1:nth-child(5)
		Snippet: <a class="rounded-xl opacity-50  p-1 hover:opacity-100" href="https://linkedin.com/in/kjaymiller">    <i class=" text-blue-900 m-1 text-2xl fa-brands fa-linkedin"></i></a>
		Messages:
		* Element does not have text that is visible to screen readers
		* aria-label attribute does not exist or is empty
		* aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
		* Element has no title attribute
		* Element is in tab order and does not have accessible text

	4)	Target: a[href$="blog.rss"]
		Snippet: <a class="hover:underline" href="/blog.rss"><span class="icon"><i class="fas fa-rss" aria-hidden="true"></i></span></a>
		Messages:
		* Element does not have text that is visible to screen readers
		* aria-label attribute does not exist or is empty
		* aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
		* Element has no title attribute
		* Element is in tab order and does not have accessible text

	5)	Target: .p-1:nth-child(2)
		Snippet: <a class="p-1" href="https://www.youtube.com/channel/UCjoJU65IbXkKXsNqydro05Q/">    <i class="text-red-700 text-2xl m-1 fa-brands fa-youtube"></i></a>
		Messages:
		* Element does not have text that is visible to screen readers
		* aria-label attribute does not exist or is empty
		* aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
		* Element has no title attribute
		* Element is in tab order and does not have accessible text

	6)	Target: .rounded-xl.opacity-50[href$="kjaymiller"]:nth-child(3)
		Snippet: <a class="rounded-xl opacity-50 p-1 hover:opacity-100" href="https://twitter.com/kjaymiller">    <i class=" text-blue-500 m-1 text-2xl fa-brands fa-twitter-square"></i></a>
		Messages:
		* Element does not have text that is visible to screen readers
		* aria-label attribute does not exist or is empty
		* aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
		* Element has no title attribute
		* Element is in tab order and does not have accessible text

	7)	Target: .lg\:flex > div > .rounded-xl.opacity-50.p-1:nth-child(4)
		Snippet: <a class="rounded-xl opacity-50  p-1 hover:opacity-100" href="https://linkedin.com/in/kjaymiller">    <i class=" text-blue-900 m-1 text-2xl fa-brands fa-linkedin"></i></a>
		Messages:
		* Element does not have text that is visible to screen readers
		* aria-label attribute does not exist or is empty
		* aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
		* Element has no title attribute
		* Element is in tab order and does not have accessible text
Rule Violated:
region - Ensures all page content is contained by landmarks
	URL: https://dequeuniversity.com/rules/axe/4.4/region?application=axeAPI
	Impact Level: moderate
	Tags: ['cat.keyboard', 'best-practice']
	Elements Affected:


	1)	Target: .bg-gradient-to-br
		Snippet: <div class="  bg-gradient-to-br    from-purple-600to-indigo-800  flex  flex-wrap  items-baseline  px-5  py-2  ">
		Messages:
		* Some page content is not contained by landmarks

	2)	Target: .flex-grow
		Snippet: <div class="flex-grow mx-2 md:mx-auto container">
		Messages:
		* Some page content is not contained by landmarks

