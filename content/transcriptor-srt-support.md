---
title: Transcriptor now Supports SRT Upload and Conversion
date: 05 Aug 2020 13:37
tags: update, accessibility
category: Transcriptor
image: https://s3-us-west-2.amazonaws.com/kjaymiller/images/Transcriptor%20Logo%20V1.1.png
---

A few weeks ago, I was tasked with a new transcription project.

The project was to create subtitles for a few videos with the intention of expanding the job to several hours of work if the work was good enough quality. While I was certain that I could figure it out, _Transcriptor_ was designed for custom text templates, not the standard SRT format. So instead of doing manual conversion of these files I decided to put the work in to make _Transcriptor_ support both the importing and exporting of SRT files. This meant also for the first time working with the end_times in text markers and focusing on getting timing down to the exact word. 

While there were wonderful options to work with SRT files I knew that I would want to build my own variation of an SRT engine. This was mostly because of future plans for transcriptor which for the first time I'm putting out there. 


You can create a `Job` object from an srt using `Job.from_srt()`. and passing in the filepath of the object.

```python
from transcriptor import Job

NewSRTJob = Job.from_srt('./srt_file.srt')
```

This give you the ability to create new objects from this job (currently a text transcription file). You also have the ability to break down the transcription word by word and by marker. This gives you the ability to apply shifts to all or some of the srt files without having to re-index the project.

```python
for marker in NewSRTJob.markers:
	marker.start_time += 2.0
	marker.end_time -= 2.0

Path('shifted_srt_file.srt').write_text(NewSRTJob.srt)
```

SRT support is avaiable on versions of _Transcriptor_ since the version series of 2020.07. You can start using _Transcriptor_ by installing the package from PyPI.

`pip install transcriptor`
