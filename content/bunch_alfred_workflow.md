---
Title: Quickly Set Your Environment with Bunch and Alfred
Tags: Brett Terpstra, Bunch, Alfred, Workflow
Date: October 01, 2019 11:00AM
---

[Bunch](https://brettterpstra.com/projects/bunch/) is an environment setup/teardown tool by the [mad genius and yoga maestro of the internet][0] Brett Terpstra.

Bunch uses small configuration files to quickly manipulate your desktop environment. 

With it you can:

* Open/Close/Focus Applications, Files, and URLs
* Run shell and Applescript scripts to expand the functionality event more

Because I prefer to keep my hands on the keyboard and the Application's main method of use is the Dock, I opted to take advantage of Bunch's URL-Scheme. 

```
x-bunch://open?bunch=[Bunch Name]
```

This plus smart use of the [_File Filter_][1] in Alfred's workflow feature allowed me to quickly setup an [Alfred Workflow][2] that not only lets you run your bunches but also lets you:

* Display the Config File of the Bunch.
* Edit the Bunch in your default application.
* Refresh your Bunches (After making a change)

The workflow is available on [Packal][3] to modify via my [Github Repo][2]

[0]: https://productivityintech.transistor.fm/episodes/podcast-ground-surfing-with-brett-terpstra
[1]: https://www.alfredapp.com/help/workflows/inputs/file-filter/
[2]: https://github.com/kjaymiller/Bunch_Alfred
[3]: http://www.packal.org/workflow/bunch-quick-launch
