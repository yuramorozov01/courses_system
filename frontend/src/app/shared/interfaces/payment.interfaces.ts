export interface IClientSecret {
    client_secret: string;
}

export interface ICardList {
    id: number;
    funding: string;
    pm_id: string;
    name: string;
    brand: string;
    exp_month: number;
    exp_year: number;
    last4: string;
}

export interface IPaymentResult {
    status: string;
    amount: number;
    currency: string;
}
