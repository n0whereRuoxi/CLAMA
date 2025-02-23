( define ( tasks blocks-tasks )
    ( :task TASK-ON-BLOCK-BLOCK
        :parameters
        (
            ?block - block
            ?block - block
        )
        :precondition
        (
        )
        :effect
        ( and
            ( on ?block ?block )
        )
    )
    
    ( :task TASK-CLEAR-BLOCK
        :parameters
        (
            ?block - block
        )
        :precondition
        (
        )
        :effect
        ( and
            ( clear ?block )
        )
    )
    
    ( :task TASK-ON-TABLE-BLOCK
        :parameters
        (
            ?table - table
            ?block - block
        )
        :precondition
        (
        )
        :effect
        ( and
            ( on ?table ?block )
        )
    )
    
    ( :task TASK-HOLDING-BLOCK
        :parameters
        (
            ?block - block
        )
        :precondition
        (
        )
        :effect
        ( and
            ( holding ?block )
        )
    )
    )