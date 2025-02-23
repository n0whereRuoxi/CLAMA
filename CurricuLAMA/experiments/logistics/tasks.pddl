( define ( tasks logistics-tasks )
    ( :task TASK-IN-TRUCK-OBJ-TRUCK
        :parameters
        (
            ?truck - truck
            ?obj - obj
            ?truck - truck
        )
        :precondition
        (
        )
        :effect
        ( and
            ( in ?truck ?obj ?truck )
        )
    )
    
    ( :task TASK-TRUCK-AT-TRUCK-LOCATION
        :parameters
        (
            ?at - at
            ?truck - truck
            ?location - location
        )
        :precondition
        (
        )
        :effect
        ( and
            ( truck ?at ?truck ?location )
        )
    )
    
    ( :task TASK-OBJ-AT-OBJ-LOCATION
        :parameters
        (
            ?at - at
            ?obj - obj
            ?location - location
        )
        :precondition
        (
        )
        :effect
        ( and
            ( obj ?at ?obj ?location )
        )
    )
    
    ( :task TASK-AIRPLANE-AT-AIRPLANE-LOCATION
        :parameters
        (
            ?at - at
            ?airplane - airplane
            ?location - location
        )
        :precondition
        (
        )
        :effect
        ( and
            ( airplane ?at ?airplane ?location )
        )
    )
    
    ( :task TASK-IN-AIRPLANE-OBJ-AIRPLANE
        :parameters
        (
            ?airplane - airplane
            ?obj - obj
            ?airplane - airplane
        )
        :precondition
        (
        )
        :effect
        ( and
            ( in ?airplane ?obj ?airplane )
        )
    )
    )