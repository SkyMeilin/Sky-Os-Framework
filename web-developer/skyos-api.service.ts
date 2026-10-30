import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface TranslationPayload {
  text: string;
  target_language?: string;
}

export interface AvatarPayload {
  avatar_id?: string;
  script_text: string;
  output_resolution?: string;
}

export interface ApiResponse {
  status: string;
  module?: string;
  audit_hash?: string;
  [key: string]: any;
}

@Injectable({
  providedIn: 'root'
})
export class SkyOsApiService {
  private readonly baseUrl = 'http://localhost:8000';
  private readonly apiKey = 'sky_sec_master_key_2026'; // Konfigurierbar via environment.ts

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'x-api-key': this.apiKey
    });
  }

  getHealth(): Observable<ApiResponse> {
    return this.http.get<ApiResponse>(`${this.baseUrl}/health`);
  }

  translateContent(payload: TranslationPayload): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(
      `${this.baseUrl}/agent/translate`,
      payload,
      { headers: this.getHeaders() }
    );
  }

  dispatchAvatarProduction(payload: AvatarPayload): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(
      `${this.baseUrl}/agent/sky-os-avatare`,
      payload,
      { headers: this.getHeaders() }
    );
  }
}
