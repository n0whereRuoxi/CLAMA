(define (problem random-logistics-c3-s2-p1-a1)
  (:domain logistics)
  ( :requirements :strips :typing :equality )
  (:objects 
    a0 - airplane
    c0 - city
    c1 - city
    c2 - city
    t0 - truck
    t1 - truck
    t2 - truck
    l0-0 - location
    l0-1 - location
    l1-0 - location
    l1-1 - location
    l2-0 - location
    l2-1 - location
    p0 - obj
  )
  (:init
    (airport l0-0)
    (airport l1-0)
    (airport l2-0)
    (in-city  l0-0 c0)
    (in-city  l0-1 c0)
    (in-city  l1-0 c1)
    (in-city  l1-1 c1)
    (in-city  l2-0 c2)
    (in-city  l2-1 c2)
    (truck-at t0 l0-0)
    (truck-at t1 l1-1)
    (truck-at t2 l2-0)
    (obj-at p0 l0-0)
    (airplane-at a0 l0-0)
  )
  (:goal
    (and
    (in-airplane p0 a0)
    )
  )
)


