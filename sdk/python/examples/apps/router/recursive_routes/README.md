# Recursive routes

A toy folder browser. The recursive `:name` route matches itself as its
own descendant, so the navigation stack grows one View per consumed URL
segment — `/folder/a/b/c` yields a stack of four views (Folders, a, a/b,
a/b/c). Back-swipe or AppBar back walks one segment at a time.

The recursive route declares a non-recursive `search` child once, and
the matcher tries non-recursive siblings before self-recursion — so
`/folder/anything/search` always lands on the `Search` page, never on
a folder named "search".

## Run

```bash
flet run
```

## What to try

1. From `/`, open `/folder` → tap a top-level folder → tap a child →
   tap another. Each step pushes a View. Back walks one level at a
   time.
2. Paste `/folder/a/b/c/d` directly into the URL → stack rebuilds with
   five Views. Back walks each.
3. From any folder, tap "Search here" → lands on the Search page below
   the current folder. Back returns there.
4. Paste `/folder/docs/projects/search` directly → stack is
   `[Folders, docs, projects, Search]`. The recursive `:name` route
   does NOT eat the "search" segment because the non-recursive
   sibling matches first.
