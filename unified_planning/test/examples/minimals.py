# Copyright 2021-2023 AIPlan4EU project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unified_planning as up
from unified_planning.shortcuts import *
from collections import namedtuple

Example = namedtuple("Example", ["problem", "plan"])


def get_example_problems():
    problems = {}

    # basic
    x = Fluent("x")
    a = InstantaneousAction("a")
    a.add_precondition(Not(x))
    a.add_effect(x, True)
    problem = Problem("basic")
    problem.add_fluent(x)
    problem.add_action(a)
    problem.set_initial_value(x, False)
    problem.add_goal(x)
    plan = up.plans.SequentialPlan([up.plans.ActionInstance(a)])
    basic = Example(problem=problem, plan=plan)
    problems["basic"] = basic

    # basic conditional
    x = Fluent("x")
    y = Fluent("y")
    a_x = InstantaneousAction("a_x")
    a_y = InstantaneousAction("a_y")
    a_x.add_precondition(Not(x))
    a_x.add_effect(x, True, y)
    a_y.add_precondition(Not(y))
    a_y.add_effect(y, True)
    problem = Problem("basic_conditional")
    problem.add_fluent(x)
    problem.add_fluent(y)
    problem.add_action(a_x)
    problem.add_action(a_y)
    problem.set_initial_value(x, False)
    problem.set_initial_value(y, False)
    problem.add_goal(x)
    plan = up.plans.SequentialPlan(
        [up.plans.ActionInstance(a_y), up.plans.ActionInstance(a_x)]
    )
    basic_conditional = Example(problem=problem, plan=plan)
    problems["basic_conditional"] = basic_conditional

    # basic oversubscription
    x = Fluent("x")
    a = InstantaneousAction("a")
    a.add_precondition(Not(x))
    a.add_effect(x, True)
    problem = Problem("basic_oversubscription")
    problem.add_fluent(x)
    problem.add_action(a)
    problem.set_initial_value(x, False)
    qm = up.model.metrics.Oversubscription({FluentExp(x): 10})
    problem.add_quality_metric(qm)
    plan = up.plans.SequentialPlan([up.plans.ActionInstance(a)])
    basic_oversubscription = Example(problem=problem, plan=plan)
    problems["basic_oversubscription"] = basic_oversubscription

    # complex conditional
    fluent_a = Fluent("fluent_a")
    fluent_b = Fluent("fluent_b")
    fluent_c = Fluent("fluent_c")
    fluent_d = Fluent("fluent_d")
    fluent_k = Fluent("fluent_k")
    fluent_x = Fluent("fluent_x")
    fluent_y = Fluent("fluent_y")
    fluent_z = Fluent("fluent_z")
    a_act = InstantaneousAction("act")
    a_0_act = InstantaneousAction("act_0")
    a_1_act = InstantaneousAction("act_1")
    a_2_act = InstantaneousAction("act_2")
    a_act.add_precondition(Not(fluent_a))
    a_act.add_effect(fluent_a, TRUE())
    a_act.add_effect(fluent_k, TRUE(), fluent_b)
    a_act.add_effect(fluent_x, TRUE(), Not(fluent_c))
    a_act.add_effect(fluent_y, FALSE(), fluent_d)
    a_0_act.add_precondition(Not(fluent_a))
    a_0_act.add_precondition(fluent_d)
    a_0_act.add_effect(fluent_b, TRUE())
    a_1_act.add_precondition(Not(fluent_a))
    a_1_act.add_precondition(fluent_d)
    a_1_act.add_precondition(fluent_b)
    a_1_act.add_effect(fluent_c, FALSE(), fluent_c)
    a_1_act.add_effect(fluent_c, TRUE(), Not(fluent_c))
    a_2_act.add_effect(fluent_a, FALSE())
    a_2_act.add_effect(fluent_d, TRUE())
    a_2_act.add_effect(fluent_z, FALSE(), fluent_z)
    a_2_act.add_effect(fluent_z, TRUE(), Not(fluent_z))
    problem = Problem("complex_conditional")
    problem.add_fluent(fluent_a)
    problem.add_fluent(fluent_b)
    problem.add_fluent(fluent_c)
    problem.add_fluent(fluent_d)
    problem.add_fluent(fluent_k)
    problem.add_fluent(fluent_x)
    problem.add_fluent(fluent_y)
    problem.add_fluent(fluent_z)
    problem.add_action(a_act)
    problem.add_action(a_0_act)
    problem.add_action(a_1_act)
    problem.add_action(a_2_act)
    problem.set_initial_value(fluent_a, True)
    problem.set_initial_value(fluent_b, False)
    problem.set_initial_value(fluent_c, True)
    problem.set_initial_value(fluent_d, False)
    problem.set_initial_value(fluent_k, False)
    problem.set_initial_value(fluent_x, False)
    problem.set_initial_value(fluent_y, True)
    problem.set_initial_value(fluent_z, False)
    problem.add_goal(fluent_a)
    problem.add_goal(fluent_b)
    problem.add_goal(Not(fluent_c))
    problem.add_goal(fluent_d)
    problem.add_goal(fluent_k)
    problem.add_goal(fluent_x)
    problem.add_goal(Not(fluent_y))
    problem.add_goal(fluent_z)
    plan = up.plans.SequentialPlan(
        [
            up.plans.ActionInstance(a_2_act),
            up.plans.ActionInstance(a_0_act),
            up.plans.ActionInstance(a_1_act),
            up.plans.ActionInstance(a_act),
        ]
    )
    complex_conditional = Example(problem=problem, plan=plan)
    problems["complex_conditional"] = complex_conditional

    # basic without negative preconditions
    x = Fluent("x")
    y = Fluent("y")
    a = InstantaneousAction("a")
    a.add_precondition(y)
    a.add_effect(x, True)
    problem = Problem("basic_without_negative_preconditions")
    problem.add_fluent(x)
    problem.add_fluent(y)
    problem.add_action(a)
    problem.set_initial_value(x, False)
    problem.set_initial_value(y, True)
    problem.add_goal(x)
    plan = up.plans.SequentialPlan([up.plans.ActionInstance(a)])
    basic_without_negative_preconditions = Example(problem=problem, plan=plan)
    problems[
        "basic_without_negative_preconditions"
    ] = basic_without_negative_preconditions

    # basic nested conjunctions
    problem = Problem("basic_nested_conjunctions")
    x = problem.add_fluent("x")
    y = problem.add_fluent("y")
    z = problem.add_fluent("z")
    j = problem.add_fluent("j")
    k = problem.add_fluent("k")

    a = InstantaneousAction("a")
    a.add_precondition(And(y, And(z, j, k)))
    a.add_effect(x, True)
    problem.add_action(a)
    problem.set_initial_value(x, False)
    problem.set_initial_value(y, True)
    problem.set_initial_value(z, True)
    problem.set_initial_value(j, True)
    problem.set_initial_value(k, True)
    problem.add_goal(And(x, And(y, z, And(j, k))))
    plan = up.plans.SequentialPlan([up.plans.ActionInstance(a)])
    basic_nested_conjunctions = Example(problem=problem, plan=plan)
    problems["basic_nested_conjunctions"] = basic_nested_conjunctions

    # basic exists
    sem = UserType("Semaphore")
    x = Fluent("x")
    y = Fluent("y", BoolType(), semaphore=sem)
    o1 = Object("o1", sem)
    o2 = Object("o2", sem)
    s_var = Variable("s", sem)
    a = InstantaneousAction("a")
    a.add_precondition(Exists(FluentExp(y, [s_var]), s_var))
    a.add_effect(x, True)
    problem = Problem("basic_exists")
    problem.add_fluent(x)
    problem.add_fluent(y)
    problem.add_object(o1)
    problem.add_object(o2)
    problem.add_action(a)
    problem.set_initial_value(x, False)
    problem.set_initial_value(y(o1), True)
    problem.set_initial_value(y(o2), False)
    problem.add_goal(x)
    plan = up.plans.SequentialPlan([up.plans.ActionInstance(a)])
    basic_exists = Example(problem=problem, plan=plan)
    problems["basic_exists"] = basic_exists

    # basic forall
    sem = UserType("Semaphore")
    x = Fluent("x")
    y = Fluent("y", BoolType(), semaphore=sem)
    s_var = Variable("s", sem)
    a = InstantaneousAction("a")
    a.add_precondition(Forall(Not(y(s_var)), s_var))
    a.add_effect(x, True)
    problem = Problem("basic_forall")
    problem.add_fluent(x)
    problem.add_fluent(y)
    o1 = problem.add_object("o1", sem)
    o2 = problem.add_object("o2", sem)
    problem.add_action(a)
    problem.set_initial_value(x, False)
    problem.set_initial_value(y(o1), False)
    problem.set_initial_value(y(o2), False)
    problem.add_goal(x)
    plan = up.plans.SequentialPlan([up.plans.ActionInstance(a)])
    basic_forall = Example(problem=problem, plan=plan)
    problems["basic_forall"] = basic_forall

    # temporal conditional
    Obj = UserType("Obj")
    is_same_obj = Fluent("is_same_obj", BoolType(), object_1=Obj, object_2=Obj)
    is_ok = Fluent("is_ok", BoolType(), test=Obj)
    is_ok_giver = Fluent("is_ok_giver", BoolType(), test=Obj)
    ok_given = Fluent("ok_given")
    set_giver = DurativeAction("set_giver", param_y=Obj)
    param_y = set_giver.parameter("param_y")
    set_giver.set_fixed_duration(2)
    set_giver.add_condition(StartTiming(), Not(is_ok_giver(param_y)))
    set_giver.add_effect(StartTiming(), is_ok_giver(param_y), True)
    set_giver.add_effect(EndTiming(), is_ok_giver(param_y), False)
    take_ok = DurativeAction("take_ok", param_x=Obj, param_y=Obj)
    param_x = take_ok.parameter("param_x")
    param_y = take_ok.parameter("param_y")
    take_ok.set_fixed_duration(3)
    take_ok.add_condition(StartTiming(), Not(is_ok(param_x)))
    take_ok.add_condition(StartTiming(), Not(is_ok_giver(param_y)))
    take_ok.add_condition(
        StartTiming(), Not(FluentExp(is_same_obj, [param_x, param_y]))
    )
    take_ok.add_effect(EndTiming(), is_ok(param_x), True, is_ok_giver(param_y))
    take_ok.add_effect(EndTiming(), ok_given, True)
    o1 = Object("o1", Obj)
    o2 = Object("o2", Obj)
    problem = Problem("temporal_conditional")
    problem.add_fluent(is_same_obj, default_initial_value=False)
    problem.add_fluent(is_ok, default_initial_value=False)
    problem.add_fluent(is_ok_giver, default_initial_value=False)
    problem.add_fluent(ok_given, default_initial_value=False)
    problem.add_action(set_giver)
    problem.add_action(take_ok)
    problem.add_object(o1)
    problem.add_object(o2)
    problem.add_goal(is_ok(o1))
    problem.set_initial_value(is_same_obj(o1, o1), True)
    problem.set_initial_value(is_same_obj(o2, o2), True)
    t_plan = up.plans.TimeTriggeredPlan(
        [
            (
                Fraction(0, 1),
                up.plans.ActionInstance(take_ok, (ObjectExp(o1), ObjectExp(o2))),
                Fraction(3, 1),
            ),
            (
                Fraction(1, 1),
                up.plans.ActionInstance(set_giver, (ObjectExp(o2),)),
                Fraction(2, 1),
            ),
        ]
    )
    temporal_conditional = Example(problem=problem, plan=t_plan)
    problems["temporal_conditional"] = temporal_conditional

    # basic with actions cost
    x = Fluent("x")
    y = Fluent("y")
    act_a = InstantaneousAction("a")
    act_a.add_precondition(Not(x))
    act_a.add_effect(x, True)
    act_b = InstantaneousAction("act_b")
    act_b.add_precondition(Not(y))
    act_b.add_effect(y, True)
    act_c = InstantaneousAction("act_c")
    act_c.add_precondition(y)
    act_c.add_effect(x, True)
    problem = Problem("basic_with_costs")
    problem.add_fluent(x)
    problem.add_fluent(y)
    problem.add_action(act_a)
    problem.add_action(act_b)
    problem.add_action(act_c)
    problem.set_initial_value(x, False)
    problem.set_initial_value(y, False)
    problem.add_goal(x)
    problem.add_quality_metric(
        up.model.metrics.MinimizeActionCosts(
            {act_a: Int(10), act_b: Int(1), act_c: Int(1)}
        )
    )
    plan = up.plans.SequentialPlan(
        [up.plans.ActionInstance(act_b), up.plans.ActionInstance(act_c)]
    )
    basic_with_costs = Example(problem=problem, plan=plan)
    problems["basic_with_costs"] = basic_with_costs

    # counter
    counter_1 = Fluent("counter_1", IntType(0, 10))
    counter_2 = Fluent("counter_2", IntType(0, 10))
    fake_counter = Fluent("fake_counter", RealType(0, 10))
    increase = InstantaneousAction("increase")
    increase.add_increase_effect(counter_1, 1)
    increase.add_effect(counter_2, Plus(counter_2, 1))
    increase.add_effect(fake_counter, Div(Times(fake_counter, 2), 2))
    problem = Problem("counter")
    problem.add_fluent(counter_1)
    problem.add_fluent(counter_2)
    problem.add_fluent(fake_counter)
    problem.add_action(increase)
    problem.set_initial_value(counter_1, 0)
    problem.set_initial_value(counter_2, 0)
    problem.set_initial_value(fake_counter, 1)
    problem.add_goal(Iff(LT(fake_counter, counter_1), LT(counter_2, 3)))
    plan = up.plans.SequentialPlan(
        [up.plans.ActionInstance(increase), up.plans.ActionInstance(increase)]
    )
    counter = Example(problem=problem, plan=plan)
    problems["counter"] = counter

    # counter to 50
    counter_f = Fluent("counter", IntType(0, 100))
    increase = InstantaneousAction("increase")
    increase.add_increase_effect(counter_f, 1)
    problem = Problem("counter_to_50")
    problem.add_fluent(counter_f)
    problem.add_action(increase)
    problem.set_initial_value(counter_f, 0)
    problem.add_goal(Equals(counter_f, 50))
    # Make a plan of 50 action instances of "increase"
    plan = up.plans.SequentialPlan(
        [up.plans.ActionInstance(increase) for _ in range(50)]
    )
    counter_to_50 = Example(problem=problem, plan=plan)
    problems["counter_to_50"] = counter_to_50

    # basic with object constant
    Location = UserType("Location")
    is_at = Fluent("is_at", BoolType(), loc=Location)
    l1 = Object("l1", Location)
    l2 = Object("l2", Location)
    move = InstantaneousAction("move", l_from=Location, l_to=Location)
    l_from = move.parameter("l_from")
    l_to = move.parameter("l_to")
    move.add_precondition(is_at(l_from))
    move.add_precondition(Not(is_at(l_to)))
    move.add_effect(is_at(l_from), False)
    move.add_effect(is_at(l_to), True)
    move_to_l1 = InstantaneousAction("move_to_l1", l_from=Location)
    l_from = move_to_l1.parameter("l_from")
    move_to_l1.add_precondition(is_at(l_from))
    move_to_l1.add_precondition(Not(is_at(l1)))
    move_to_l1.add_effect(is_at(l_from), False)
    move_to_l1.add_effect(is_at(l1), True)
    problem = Problem("basic_with_object_constant")
    problem.add_fluent(is_at)
    problem.add_objects([l1, l2])
    problem.add_action(move)
    problem.add_action(move_to_l1)
    problem.set_initial_value(is_at(l1), True)
    problem.set_initial_value(is_at(l2), False)
    problem.add_goal(is_at(l2))
    plan = up.plans.SequentialPlan(
        [up.plans.ActionInstance(move, (ObjectExp(l1), ObjectExp(l2)))]
    )
    basic_with_object_constant = Example(problem=problem, plan=plan)
    problems["basic_with_object_constant"] = basic_with_object_constant

    # basic numeric
    value = Fluent("value", IntType())
    task = InstantaneousAction("task")
    task.add_precondition(Equals(value, 1))
    task.add_effect(value, 2)
    problem = Problem("basic_numeric")
    problem.add_fluent(value)
    problem.add_action(task)
    problem.set_initial_value(value, 1)
    problem.add_goal(Equals(value, 2))
    plan = up.plans.SequentialPlan([up.plans.ActionInstance(task)])
    problems["basic_numeric"] = Example(problem=problem, plan=plan)

    return problems
