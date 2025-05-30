#let title = "Behavior of Merge Sort implemented with MPI"
#let subject = (
	code: "CSC175",
	desc: "Parallel and Distributed Computing"
)

#import "@preview/codelst:2.0.2": sourcecode

// Formatting pages
#set page(
	paper: "us-legal",
	margin: (x: 0.75in, y: 1in),
	numbering: "1/1",
	number-align: right,
	header: [*#subject.code* #subject.desc]
)

// Format paragraphs
#set par(
	justify: true
)

// TITLE
#align(
	center,
)[
	#line(length: 100%, stroke: 0.5pt)
	#v(0.5em)
	#text(20pt)[#smallcaps(title)],
	#v(0.5em)
	#line(length: 90%, stroke: 0.5pt)
]

#align(
	center,
	text()[*Ahmad Badron*\
	BS Computer Science\
	Mindanao State University]
)

#grid(
	columns: (1cm,1fr,1cm),
	// fill: yellow,
	column-gutter: 2pt,
	[],
	[*Abstract*: #lorem(100)]
)

#v(1em)
#line(length: 100%, stroke: 0.5pt)
#v(1em)

#show: rest => columns(2, rest)
// #set page(columns: 2)

#show outline.entry: it => link(
	it.element.location(),
	it.indented(it.prefix(), it.body())
)
#outline()

#include "01 intro.typ"
#include "02 methods.typ"
#include "03 results.typ"
#include "04 conclusion.typ"


// Appendix
#include "appendix.typ"
#bibliography("refs.bib",title: "Bibliography")