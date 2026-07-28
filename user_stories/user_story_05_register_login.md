# User story 05: Register, log in & log out

*As a customer, I want to create an account and sign in so that my details and orders are
remembered — while still being able to check out as a guest.*

## Priority: P1 (highest) — Iteration 2

## Estimation: 1.5 days
Planning poker (all four members):
* Etigel: 1 · Kei: 2 · Samuel: 2 · Shane: 1
* **Agreed: 1.5 days** (email-as-username and guest-checkout coexistence discussed)

## Assumptions
* Sign-in is by **email + password** (email stored as the username).
* Guest checkout must still work — accounts are optional.

## Description
A combined sign-in / register page (tabbed) lets a user create an account or log in; the header
then shows *My orders* and *Log out*. Orders placed while logged in are linked to the account.
A "continue as guest" link preserves guest checkout.

## Tasks
1. `login_register` view (login + register, validation), 0.6 d
2. Auth template (tabs, guest link) + logout, 0.4 d
3. Auth-aware header; link orders to `request.user` at checkout, 0.5 d

## UI design
INO mock-up; realised at `http://147.93.56.126:8080/account/sign-in/`.

## Completed
✅ Iteration 2. Extended by the profile/favourites stories (11–13). Open-redirect protection on
`?next=` is covered by an automated test.
