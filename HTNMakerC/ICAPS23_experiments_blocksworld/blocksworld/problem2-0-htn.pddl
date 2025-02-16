( define ( htn-problem probname )
  ( :domain blocks4 )
  ( :requirements :strips :htn :typing :equality )
  ( :objects
    b545 - block
    b438 - block
    b580 - block
  )
  ( :init
    ( hand-empty )
    ( on-table b545 )
    ( on b438 b545 )
    ( on b580 b438 )
    ( clear b580 )
  )
  ( :tasks
    ( Make-Clear b545 )
  )
)
