( define ( problem probname )

  ( :domain logistics )

  ( :requirements :strips :typing :equality )

  ( :objects
    a000 - airplane
    a001 - airplane
    c000 - city
    c001 - city
    t000-000 - truck
    t001-000 - truck
    l000-000 - location
    l000-001 - location
    l000-002 - location
    l001-000 - location
    l001-001 - location
    l001-002 - location
    p000 - obj
  )

  ( :init
    ( in-city l000-000 c000 )
    ( in-city l000-001 c000 )
    ( in-city l000-002 c000 )
    ( in-city l001-000 c001 )
    ( in-city l001-001 c001 )
    ( in-city l001-002 c001 )
    ( airport l000-000 )
    ( airport l001-000 )
    ( truck-at t000-000 l000-002 )
    ( truck-at t001-000 l001-002 )
    ( airplane-at a000 l000-000 )
    ( airplane-at a001 l001-000 )
    ( obj-at p000 l000-002 )
  )

  ( :goal
    ( and
      ( obj-at p000 l001-002 )
    )
  )
)

