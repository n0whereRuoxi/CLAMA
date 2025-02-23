( define ( domain Blocks4 )
  ( :requirements :strips :typing :equality :htn )
  ( :types block )
  ( :predicates
    ( ON-TABLE ?b - BLOCK )
    ( ON ?b1 - BLOCK ?b2 - BLOCK )
    ( CLEAR ?b - BLOCK )
    ( HAND-EMPTY )
    ( HOLDING ?b - BLOCK )
  )
  ( :action !PICKUP
    :parameters
    (
      ?b - BLOCK
    )
    :precondition
    ( and ( ON-TABLE ?b ) ( CLEAR ?b ) ( HAND-EMPTY ) )
    :effect
    ( and ( not ( ON-TABLE ?b ) ) ( not ( CLEAR ?b ) ) ( not ( HAND-EMPTY ) ) ( HOLDING ?b ) )
  )
  ( :action !PUTDOWN
    :parameters
    (
      ?b - BLOCK
    )
    :precondition
    ( and ( HOLDING ?b ) )
    :effect
    ( and ( not ( HOLDING ?b ) ) ( HAND-EMPTY ) ( ON-TABLE ?b ) ( CLEAR ?b ) )
  )
  ( :action !UNSTACK
    :parameters
    (
      ?b1 - BLOCK
      ?b2 - BLOCK
    )
    :precondition
    ( and ( ON ?b1 ?b2 ) ( CLEAR ?b1 ) ( HAND-EMPTY ) )
    :effect
    ( and ( not ( ON ?b1 ?b2 ) ) ( not ( CLEAR ?b1 ) ) ( not ( HAND-EMPTY ) ) ( CLEAR ?b2 ) ( HOLDING ?b1 ) )
  )
  ( :action !STACK
    :parameters
    (
      ?b1 - BLOCK
      ?b2 - BLOCK
    )
    :precondition
    ( and ( HOLDING ?b1 ) ( CLEAR ?b2 ) )
    :effect
    ( and ( not ( HOLDING ?b1 ) ) ( not ( CLEAR ?b2 ) ) ( HAND-EMPTY ) ( ON ?b1 ?b2 ) ( CLEAR ?b1 ) )
  )
  ( :method TASK-CLEAR-BLOCK
    :parameters
    (
      ?auto_1 - BLOCK
    )
    :vars
    (
      ?auto_2 - BLOCK
    )
    :precondition
    ( and ( ON ?auto_2 ?auto_1 ) ( CLEAR ?auto_2 ) ( HAND-EMPTY ) ( not ( = ?auto_1 ?auto_2 ) ) )
    :subtasks
    ( ( !UNSTACK ?auto_2 ?auto_1 ) )
  )

  ( :method TASK-CLEAR-BLOCK
    :parameters
    (
      ?auto_7 - BLOCK
    )
    :vars
    (
      ?auto_8 - BLOCK
      ?auto_9 - BLOCK
    )
    :precondition
    ( and ( ON ?auto_8 ?auto_7 ) ( CLEAR ?auto_8 ) ( not ( = ?auto_7 ?auto_8 ) ) ( HOLDING ?auto_9 ) ( not ( = ?auto_7 ?auto_9 ) ) ( not ( = ?auto_8 ?auto_9 ) ) )
    :subtasks
    ( ( !PUTDOWN ?auto_9 )
      ( TASK-CLEAR-BLOCK ?auto_7 ) )
  )

  ( :method TASK-CLEAR-BLOCK
    :parameters
    (
      ?auto_11 - BLOCK
    )
    :vars
    (
      ?auto_12 - BLOCK
      ?auto_13 - BLOCK
    )
    :precondition
    ( and ( ON ?auto_12 ?auto_11 ) ( not ( = ?auto_11 ?auto_12 ) ) ( not ( = ?auto_11 ?auto_13 ) ) ( not ( = ?auto_12 ?auto_13 ) ) ( ON ?auto_13 ?auto_12 ) ( CLEAR ?auto_13 ) ( HAND-EMPTY ) )
    :subtasks
    ( ( TASK-CLEAR-BLOCK ?auto_12 )
      ( TASK-CLEAR-BLOCK ?auto_11 ) )
  )

  ( :method TASK-CLEAR-BLOCK
    :parameters
    (
      ?auto_26 - BLOCK
    )
    :vars
    (
      ?auto_27 - BLOCK
      ?auto_28 - BLOCK
      ?auto_29 - BLOCK
    )
    :precondition
    ( and ( ON ?auto_27 ?auto_26 ) ( not ( = ?auto_26 ?auto_27 ) ) ( not ( = ?auto_26 ?auto_28 ) ) ( not ( = ?auto_27 ?auto_28 ) ) ( ON ?auto_28 ?auto_27 ) ( CLEAR ?auto_28 ) ( HOLDING ?auto_29 ) ( not ( = ?auto_26 ?auto_29 ) ) ( not ( = ?auto_27 ?auto_29 ) ) ( not ( = ?auto_28 ?auto_29 ) ) )
    :subtasks
    ( ( !PUTDOWN ?auto_29 )
      ( TASK-CLEAR-BLOCK ?auto_26 ) )
  )

  ( :method TASK-CLEAR-BLOCK
    :parameters
    (
      ?auto_31 - BLOCK
    )
    :vars
    (
      ?auto_33 - BLOCK
      ?auto_32 - BLOCK
      ?auto_34 - BLOCK
    )
    :precondition
    ( and ( ON ?auto_33 ?auto_31 ) ( not ( = ?auto_31 ?auto_33 ) ) ( not ( = ?auto_31 ?auto_32 ) ) ( not ( = ?auto_33 ?auto_32 ) ) ( ON ?auto_32 ?auto_33 ) ( not ( = ?auto_31 ?auto_34 ) ) ( not ( = ?auto_33 ?auto_34 ) ) ( not ( = ?auto_32 ?auto_34 ) ) ( ON ?auto_34 ?auto_32 ) ( CLEAR ?auto_34 ) ( HAND-EMPTY ) )
    :subtasks
    ( ( TASK-CLEAR-BLOCK ?auto_32 )
      ( TASK-CLEAR-BLOCK ?auto_31 ) )
  )

)
