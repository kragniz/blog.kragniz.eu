Lightning Lightning Talks at FOSDEM 2025
########################################
:date: 2025-02-16 16:00
:author: Louis Taylor
:category: fosdem
:tags: fosdem, conferences
:slug: fosdem-lightning-lightning-talks

For the last few years I've been running the lightning talk track at
`FOSDEM <https://fosdem.org>`_.

This track contains a series of 15 minute talks separated by 5 minute breaks
all day, a format which has been mostly unchanged since its first `introduction in
2007
<https://archive.fosdem.org/2007/schedule/tracks/lightningtalks.html>`_, 18
years ago:

.. image:: {static}/images/2007-lightning-talks.png
   :target: https://archive.fosdem.org/2007/schedule/tracks/lightningtalks.html
   :alt: Screenshot of FOSDEM 2007 lightning talk schedule

There are some advantages to this format:

* listing each talk in the schedule allows people to attend a single talk which interests them, then leave
* 5 minute gaps between talks allow for more tolerance towards technical difficulties
* can be handled like any other talk in the program

And some (subjective) disadvantages:

* different from what people would expect "lightning talks" to mean compared to other events
* 15 minutes is actually quite a long time, and preparing a good talk of this length requires some effort
* more effort makes it harder to spontaneously prepare a talk, and riskier to accept a hastily prepared talk into the schedule
* some speakers prepare a talk which takes less than 15 minutes, so someone watching a series of talks might see 10 minutes of talk, followed by 10 minutes of gap before the next talk

For better or for worse, the average talk length at FOSDEM has also been steadily decreasing over the years.
If we extrapolate this trend into the future, talks in the current lightning
talk track will at some point be longer than the average talk elsewhere!

.. image:: {static}/images/fosdem-talk-length.svg
   :alt: Plot of year and average talk length

This clearly makes the case for something which contains even more lightning
than the usual lightning talks.

For FOSDEM 2025, I wanted to make something with the following goals:

#. A single session with no downtime
#. Felt spontaneous
#. Entertaining to watch
#. Low bar for entry

Normally this kind of session at a conference would just be called "lightning
talks", but we already have the existing lightning talks track which wouldn't
be changing this year.

Since the main difference between them is the quantity of lightning involved, I named it
Lightning Lightning Talks instead.

The software
------------

To run this session, something needed to:

#. Let people submit talk proposals with slides attached
#. Review and accept some talks
#. On the day of the session, grab the slides for accepted talks
#. Display a title screen to make sure the right speaker starts speaking
#. Display presentation slides
#. Count how long a speaker has left
#. Move to the next talk once time has run out

The first two points are covered by `pretalx
<https://github.com/pretalx/pretalx>`_, the tool used for all the normal
proposal management at FOSDEM. The only complication was making it easy to get
the list of accepted talks and the attached slides. This ended up being a new track in
pretalx, and also a new proposal type to make filtering using the pretalx API
possible.

A tool could then be written to query the API for the data about talks and
write an intermediate config file describing the required info for the upcoming
session. Since there's a much higher chance of changes at the last minute (for
example some speakers not turning up), keeping the info for the session in a
format which could be quickly edited by hand was important. It also removes a
hard dependency on our pretalx deployment, so the session can run even if
pretalx is down for some reason.

This file is a fairly unexciting ``.json`` file, and looks about the same as you would expect:

.. code-block:: json

    [
      {
        "title": "Zagreb City case study: How to foster open data with public money",
        "speakers": "Aleksandar Gavrilovic",
        "slides_url": "https://pretalx.fosdem.org/media/fosdem-2025/submissions/8NP3TN/resources/Zagreb_Ca_ryBYjbT.pdf",
        "slides_name": "Zagreb_Ca_ryBYjbT.pdf",
        "created": "2025-01-20T09:32:48.352004+01:00"
      },
      {
        "title": "A Card Game for you techies",
        "speakers": "Thierry Berger",
        "slides_url": "https://pretalx.fosdem.org/media/fosdem-2025/submissions/DXRMQC/resources/pitch_kln5nRa.pdf",
        "slides_name": "pitch_kln5nRa.pdf",
        "created": "2025-01-28T09:29:02.942777+01:00"
      },


I wrote a custom presentation tool which reads this ``.json`` and uses it to
display a neat title screen for each talk followed by the slides provided by
each speaker. This uses GTK for the main application and Pango + Cairo to
render most of the graphics.

To annoy everyone equally (except LaTeX users) I required slides in ``.pdf``
format, which meant I needed to render pages from them for the main
presentation content. For this I used Poppler [1]_, which ended up being pretty
easy to implement (except for spending a bit too long figuring out why a
particular presentation wasn't rendering correctly before I found out pdf
documents could be transparent and I was rendering on a black background).

Most of the time developing this tool probably went into making the title
screen look nice, with a pleasing ease in function (quint, :math:`1 - (1 - t)^5`)
animating the FOSDEM cog pulling the title on to the screen:

.. raw:: html

    <video autoplay loop muted playsinline>
      <source src="{static}/images/lightninglightning-2025-02-09_15.09.38_1.webm" type="video/webm" />
    </video>

A second window shows the time remaining for the current speaker, which can be displayed on a secondary monitor:

.. raw:: html

    <video autoplay loop muted playsinline>
      <source src="{static}/images/lightninglightning-countdown-2025-02-09_15.12.14_1.webm" type="video/webm" />
    </video>

To make sure speakers don't overstay their welcome on the stage, the system
needs to move them on. For lightning talks elsewhere, this is often done with a
separate timer and social pressure to stop. Since this custom presentation tool
knows how long the current speaker has taken and the order of talks, it can
immediately start the next talk once the time has run out.

When the time left reaches 10 seconds, the countdown screen starts flashing in
warning, while the presentation slides slowly fade out to the title screen and
the next talk begins automatically:

.. raw:: html

    <video autoplay loop muted playsinline>
      <source src="{static}/images/lightninglightning-countdown-move-to-next-2025-02-09_15.23.33_1.webm" type="video/webm" />
    </video>

Code for this tool is available at https://github.com/kragniz/fosdem-lightning-talk-presenter

.. [1] As luck would have it, there was a lightning talk at FOSDEM this year about Poppler: https://fosdem.org/2025/schedule/event/fosdem-2025-6000-poppler-the-pdf-rendering-library/

People logistics
----------------

Despite planning the actual presentation display and submission system, I
hadn't fully planned the logistics of people moving around until the evening
before the session. This meant quickly working out a system to make sure
speakers could smoothly flow from one talk to the next.

With the help of some volunteers who were assisting with running the session on
the day, we thought through a few options and settled with:

- Printing off the talk schedule, and giving a copy to each speaker just in case the order is forgotten
- Sitting speakers ``n-3`` in a row of audience seats in the same order as their position in the talk schedule
- Using two seats at the side of the stage as a staging area (#1 containing the next speaker, and #2 containing the speaker after next)
- Using two handheld microphones (one held by the current speaker, one held by the next speaker)

On a talk ending, everybody swaps to a new position simultaneously:

#. Speaker leaves the stage, handing their microphone to the person in staging area seat #2
#. Person in the #1 staging area seat takes to the stage and begins their talk
#. Person in staging area seat #2 moves to seat #1
#. Person in the rightmost seat in the audience row moves to staging area seat #2
#. All other speakers sitting in the audience row move one seat to the right

This ended up worked pretty smoothly. There was a contingency plan in case a
speaker carried on talking after their time ran out involving a volunteer
threateningly wielding a brush and sweeping them off the stage, which (somewhat
unfortunately, since it would have been entertaining) never needed to be deployed.

How it went
-----------

I was really pleased with how this worked out in the end. Running a session
which relied on custom presentation software and a large number of speakers had
the potential for some unforeseen disaster, which had made me a bit anxious. No
disasters took place, and feedback has been nice.

You can watch the recording here:

.. image:: {static}/images/lightning-lightning-title.jpg
   :target: https://fosdem.org/2025/schedule/event/fosdem-2025-6674-lightning-lightning-talks/
   :alt: Screenshot of FOSDEM 2007 lightning talk schedule

The talks were good. Someone was enthusiastic about isopods:

.. raw:: html

   <blockquote class="mastodon-embed" data-embed-url="https://chaos.social/@whatareyoudoinginmyswamp/113947154552710824/embed" style="background: #FCF8FF; border-radius: 8px; border: 1px solid #C9C4DA; margin: 0; max-width: 540px; min-width: 270px; overflow: hidden; padding: 0;"> <a href="https://chaos.social/@whatareyoudoinginmyswamp/113947154552710824" target="_blank" style="align-items: center; color: #1C1A25; display: flex; flex-direction: column; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', Roboto, sans-serif; font-size: 14px; justify-content: center; letter-spacing: 0.25px; line-height: 20px; padding: 24px; text-decoration: none;"> <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="32" height="32" viewBox="0 0 79 75"><path d="M74.7135 16.6043C73.6199 8.54587 66.5351 2.19527 58.1366 0.964691C56.7196 0.756754 51.351 0 38.9148 0H38.822C26.3824 0 23.7135 0.756754 22.2966 0.964691C14.1319 2.16118 6.67571 7.86752 4.86669 16.0214C3.99657 20.0369 3.90371 24.4888 4.06535 28.5726C4.29578 34.4289 4.34049 40.275 4.877 46.1075C5.24791 49.9817 5.89495 53.8251 6.81328 57.6088C8.53288 64.5968 15.4938 70.4122 22.3138 72.7848C29.6155 75.259 37.468 75.6697 44.9919 73.971C45.8196 73.7801 46.6381 73.5586 47.4475 73.3063C49.2737 72.7302 51.4164 72.086 52.9915 70.9542C53.0131 70.9384 53.0308 70.9178 53.0433 70.8942C53.0558 70.8706 53.0628 70.8445 53.0637 70.8179V65.1661C53.0634 65.1412 53.0574 65.1167 53.0462 65.0944C53.035 65.0721 53.0189 65.0525 52.9992 65.0371C52.9794 65.0218 52.9564 65.011 52.9318 65.0056C52.9073 65.0002 52.8819 65.0003 52.8574 65.0059C48.0369 66.1472 43.0971 66.7193 38.141 66.7103C29.6118 66.7103 27.3178 62.6981 26.6609 61.0278C26.1329 59.5842 25.7976 58.0784 25.6636 56.5486C25.6622 56.5229 25.667 56.4973 25.6775 56.4738C25.688 56.4502 25.7039 56.4295 25.724 56.4132C25.7441 56.397 25.7678 56.3856 25.7931 56.3801C25.8185 56.3746 25.8448 56.3751 25.8699 56.3816C30.6101 57.5151 35.4693 58.0873 40.3455 58.086C41.5183 58.086 42.6876 58.086 43.8604 58.0553C48.7647 57.919 53.9339 57.6701 58.7591 56.7361C58.8794 56.7123 58.9998 56.6918 59.103 56.6611C66.7139 55.2124 73.9569 50.665 74.6929 39.1501C74.7204 38.6967 74.7892 34.4016 74.7892 33.9312C74.7926 32.3325 75.3085 22.5901 74.7135 16.6043ZM62.9996 45.3371H54.9966V25.9069C54.9966 21.8163 53.277 19.7302 49.7793 19.7302C45.9343 19.7302 44.0083 22.1981 44.0083 27.0727V37.7082H36.0534V27.0727C36.0534 22.1981 34.124 19.7302 30.279 19.7302C26.8019 19.7302 25.0651 21.8163 25.0617 25.9069V45.3371H17.0656V25.3172C17.0656 21.2266 18.1191 17.9769 20.2262 15.568C22.3998 13.1648 25.2509 11.9308 28.7898 11.9308C32.8859 11.9308 35.9812 13.492 38.0447 16.6111L40.036 19.9245L42.0308 16.6111C44.0943 13.492 47.1896 11.9308 51.2788 11.9308C54.8143 11.9308 57.6654 13.1648 59.8459 15.568C61.9529 17.9746 63.0065 21.2243 63.0065 25.3172L62.9996 45.3371Z" fill="currentColor"/></svg> <div style="color: #787588; margin-top: 16px;">Post by @whatareyoudoinginmyswamp@chaos.social</div> <div style="font-weight: 500;">View on Mastodon</div> </a> </blockquote> <script data-allowed-prefixes="https://chaos.social/" async src="https://chaos.social/embed.js"></script>


Future
------

I'd like to make some changes if we run something similar next time:

* I'd like to encourage more random and fun topics
* 5 minutes is still quite a long time! In a 50 minute session we can only fit
  10 talks if everyone takes the maximum time. Maybe next time the limit could
  be 3 minutes.
* A bigger display showing the countdown visible from the audience would be nice
* Make sure no mouse cursor is drawn over slides
* The countdown should start as soon as the title screen is shown
* A remote control to skip to the next presentation would be good, some
  speakers forgot to complete their slides all the way to the end, so the next
  speaker needed to skip forward a bit awkwardly
* Shuffling all speakers one seat over was necessary because all the seats in
  this room have built in desks which make getting in and out of a row awkward
  unless you are sitting right at the end. Obtaining extra chairs to make an
  additional row of seats at the font would avoid needing to do this.
* The submission process needs to be smoother. The extra track and submission
  type was confusing in the pretalx UI.
* The submission deadline and status needs to be communicated better. I was
  originally worried about not getting enough proposals, but ended up getting
  too many. I closed submissions early since I didn't want people to spend time
  working on a presentation if all the spaces were taken, but this (quite
  rightfully) annoyed some people since they thought there would still be time
  to submit a talk

I originally wanted to make talk order random out of a pool of people who
registered as speakers before the session begins. However this felt a bit too
risky for a first try. Perhaps some element of this could be introduced next
time?

Hopefully Lightning Lightning Talks will return next time (maybe with a name change)!
