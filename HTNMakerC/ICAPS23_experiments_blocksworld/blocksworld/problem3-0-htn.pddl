( define ( htn-problem probname )
  ( :domain blocks4 )
  ( :requirements :strips :htn :typing :equality )
  ( :objects
    b468 - block
    b762 - block
    b494 - block
    b655 - block
  )
  ( :init
    ( hand-empty )
    ( on-table b468 )
    ( on b762 b468 )
    ( on b494 b762 )
    ( on b655 b494 )
    ( clear b655 )
  )
  ( :tasks
    ( Make-Clear b468 )
  )
)
