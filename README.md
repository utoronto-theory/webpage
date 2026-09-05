# webpage
This is the repo for the UToronto theory webpage.

To contribute, you can follow the guide at: https://www.cs.toronto.edu/%7Eziyang/github.html

## Preview locally

The website is static HTML and CSS. No package installation or build step is
needed to serve it. From this directory, run:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000`. Preview changes at both phone and laptop
widths before publishing through the existing department workflow.

## Maintaining the site

- Edit page content directly in the corresponding `.html` file, inside `main`.
- Shared navigation and footer markup live in `templates/header.html` and
  `templates/footer.html`. After editing either, run `python3 scripts/update_layout.py`
  and commit the updated HTML pages along with the templates. The generated
  layout blocks are marked in each page; no runtime includes are needed.
- `site.css` contains the editorial design and responsive layouts. `js/site.js`
  enhances the mobile menu; page content and the native People menu also work
  without JavaScript. The old Inland and jQuery files are retained for provenance
  but are no longer loaded by the main pages.
- The homepage slideshow uses `js/carousel.js` and taller source versions of the
  five original photographs, filling a consistent 2:1 frame. Edit slides and
  captions directly in `index.html`. Photos advance automatically every seven
  seconds, with previous/next buttons and no Play/Pause button. Manual navigation
  resets the timer. Rotation pauses on hover or keyboard focus and resumes when
  the pointer or focus leaves; touch navigation keeps autoplay running.
  Reduced-motion settings disable autoplay; the first photograph remains visible
  without JavaScript.
- Preserve existing URLs and named anchors. `pastseminars.html` contains the
  historical seminar archive; `Corneil-bio.htm` remains the original biography.
- Keep names, interests, affiliations, application status, and dated course
  information accurate. A past application deadline does not by itself establish
  whether late applications are still accepted.

## Checks

Run these before submitting changes:

```sh
python3 scripts/check_site.py
git diff --check
```

The checker uses only the Python standard library. It checks shared-layout
consistency, page landmarks, image alternatives, local files, and fragment links.
It does not verify external websites, content currency, or full accessibility
conformance. Also check keyboard navigation, the Menu and People disclosures,
and representative pages at 320, 390, 768, and 1280 pixels. The event calendar is
provided by Google; its direct link remains available if the embed cannot load.
