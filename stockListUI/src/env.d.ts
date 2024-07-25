declare interface Env {
  readonly API_HOST: string;
  [key: string]: any;
}

declare interface ImportMeta {
  readonly env: Env;
}
