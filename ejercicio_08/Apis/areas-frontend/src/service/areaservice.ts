import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Area } from '../domain/area';
import { TableLazyLoadEvent, TablePageEvent } from 'primeng/table';

@Injectable({
    providedIn: 'root'
})
export class AreaService {

    /**
     * Define la URL del backend.
     */
    public baseUrl= '';

    constructor(private http: HttpClient) {
    }

    private buildParams(filtro: TableLazyLoadEvent): HttpParams {
        let params = new HttpParams();
        params = params.append('mode', 'paginated');

        if (filtro.rows) {
            params = params.append('per_page', filtro.rows);
        } else {
            params = params.append('per_page', 10);
        }

        if (filtro.first) {
            let per_page = filtro?.rows ?? 10;
            params = params.append('page', filtro.first / per_page + 1);
        } else {
            params = params.append('page', 1);
        }

        if (filtro?.sortField) {
            params.append('sort', filtro.sortField as string);
        }

        if (filtro?.sortOrder) {
            if (filtro?.sortOrder > 0) {
                params.append('order', 'asc');
            } else {
                params.append('order', 'desc');
            }
        }

        if (filtro?.globalFilter) {
            params.append('1', filtro.globalFilter as string);
        }


        return params;
    }

    getAll(filtro: TableLazyLoadEvent): Observable<any> {
        const httpOptions = {
            headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
            params: this.buildParams(filtro)
        };
        return this.http.get(this.baseUrl + '/area', httpOptions);
    }

    getById(idArea: number): Observable<any> {
        return this.http.get(this.baseUrl + '/area/' + idArea);
    }

    save(area: Area): Observable<any> {
        return this.http.post(this.baseUrl + '/area', area);
    }

    update(area: Area): Observable<any> {
        return this.http.put(this.baseUrl + '/area/' + area.id_area, area);
    }

    delete(idArea: number): Observable<any> {
        return this.http.delete(this.baseUrl + '/area/' + idArea);
    }

}
