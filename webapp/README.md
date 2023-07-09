# vue-project

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Set env
```sh
Create .env file and put variable with prefix VITE_
Example: VITE_APP_NAME=EasyMoney and use import.meta.env. to get env variable
```

### Auth0
```sh
Set Application Type is Single Page Application
AccessToken: This is used to access the user\'s profile and the /userinfo endpoint. It is a JWT that contains user profile information.
Token: This is used to access the Auth0 Management API and perform actions on behalf of the user. It is a JWT that contains scopes and permissions.
```