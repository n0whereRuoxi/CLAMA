( define
  ( tasks Blocks4-tasks )
  ( :task Make-Clear
    :parameters
    (
      ?b1 - block
    )
    :precondition
    (
    )
    :effect
    ( and
      ( clear ?b1 )
    )
  )
)
