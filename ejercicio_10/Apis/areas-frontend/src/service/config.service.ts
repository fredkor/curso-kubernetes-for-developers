import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {
  private config: any = {};

  constructor(private http: HttpClient) {}

  loadConfig(): Promise<void> {
    return this.http.get('/assets/config.json').toPromise()
      .then((config) => {
        this.config = config;
        console.log("✅ Config cargada:", this.config);
      })
      .catch((error) => {
        console.error("❌ Error cargando config.json", error);
      });
  }

  get(key: string): any {
    return this.config[key];
  }
}
