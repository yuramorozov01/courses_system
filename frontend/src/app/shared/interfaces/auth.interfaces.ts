export interface IUser {
    email?: string;
    username: string;
    password: string;
}

export interface IUserMe {
    email: string;
    id: number;
    username: string;
}

export interface IJWT {
    refresh: string;
    access: string;
}

export interface IAccess {
    access: string;
}

export interface IRefresh {
    refresh: string;
}
