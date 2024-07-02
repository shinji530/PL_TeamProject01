# PL_TeamProject01
프로그래밍언어론 프로젝트 LLParser

문법
----
```
<program> → <statements>

<statements>→ <statement> | <statement><semi_colon><statements>

<statement> → <ident><assignment_op><expression>

<expression> → <term><term_tail>

<term_tail> → <add_op><term><term_tail> | ε

<term> → <factor> <factor_tail>

<factor_tail> → <mult_op><factor><factor_tail> | ε

<factor> → <left_paren><expression><right_paren> | <ident> | <const>

<const> → any decimal numbers

<ident> → any names conforming to C identifier rules

<assignment_op> → :=

<semi_colon> → ;

<add_operator> → + | -

<mult_operator> → * | /

<left_paren> → (

<right_paren> → )

```
