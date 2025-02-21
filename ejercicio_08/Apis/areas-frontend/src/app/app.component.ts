import { ChangeDetectorRef, Component, ViewChild } from '@angular/core';
import { Area } from '../domain/area';
import {Table, TableLazyLoadEvent} from 'primeng/table';
import {ConfirmationService, LazyLoadEvent, MessageService} from 'primeng/api';
import { ImportsModule } from './import';
import { AreaService } from '../service/areaservice';
import {ConfigService} from '../service/config.service';


interface Column {
  field: string;
  header: string;
  customExportHeader?: string;
}

interface ExportColumn {
  title: string;
  dataKey: string;
}


@Component({
  selector: 'app-root',
  imports: [ImportsModule],
  templateUrl: './app.component.html',
  standalone: true,
  styleUrl: './app.component.css',
  providers: [MessageService, ConfirmationService, AreaService, ConfigService],
  styles: [
      `:host ::ng-deep .p-dialog .area-image {
          width: 150px;
          margin: 0 auto 2rem auto;
          display: block;
      }`
  ]
})
export class AppComponent {
  title = 'areas-frontend';

  areaDialog: boolean = false;

  areas!: Area[];

  area!: Area;

  selectedAreas!: Area[] | null;

  submitted: boolean = false;

  statuses!: any[];

  @ViewChild('dt') dt!: Table;

  cols!: Column[];

  exportColumns!: ExportColumn[];

  totalRecords = 0;

  perPage = 10;

  loading = false;


  constructor(
      private configService: ConfigService,
      private areaService: AreaService,
      private messageService: MessageService,
      private confirmationService: ConfirmationService,
      private cd: ChangeDetectorRef
  ) {
    configService.loadConfig().then(() => {
      console.log("✅ Variables listas, ya puedo usarlas.");
      console.log("🔹 API_URL:", configService.get("API_URL"));
      this.areaService.baseUrl = configService.get("API_URL");
      this.loadLazy({ first: 0, rows: 10 });
    });
  }

  loadLazy(event: TableLazyLoadEvent) {
    this.loading = true;
    this.areaService.getAll(event).subscribe(r => {
      this.areas = r.data;
      this.totalRecords = r.total;
      this.perPage = r.per_page;
      this.loading = false;
    }, e => {
      this.loading = false;
      this.messageService.add({ severity: 'error', summary: 'Error', detail:'Lazy', life: 3000 });
    });
  }

  exportCSV() {
      this.dt.exportCSV();
  }

  applyFilter(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input?.value) {
      this.dt.filterGlobal(input.value, 'contains');
    }
  }

  loadDemoData() {
    this.areaService.getAll({'rows': 1000}).subscribe(r => {
        this.areas = r;
    }, e => {
        this.messageService.add({ severity: 'error', summary: 'Error', detail: e.error.message, life: 3000 });
    });

      this.statuses = [
          { label: 'INSTOCK', value: 'instock' },
          { label: 'LOWSTOCK', value: 'lowstock' },
          { label: 'OUTOFSTOCK', value: 'outofstock' }
      ];

      this.cols = [
          { field: 'code', header: 'Code', customExportHeader: 'Area Code' },
          { field: 'name', header: 'Name' },
          { field: 'image', header: 'Image' },
          { field: 'price', header: 'Price' },
          { field: 'category', header: 'Category' }
      ];

      this.exportColumns = this.cols.map((col) => ({ title: col.header, dataKey: col.field }));
  }

  openNew() {
      this.area = {"activo": true};
      this.submitted = false;
      this.areaDialog = true;
  }

  editArea(area: Area) {
      this.area = { ...area };
      this.areaDialog = true;
  }

  deleteSelectedAreas() {
      this.confirmationService.confirm({
          message: 'Are you sure you want to delete the selected products?',
          header: 'Confirm',
          icon: 'pi pi-exclamation-triangle',
          accept: () => {
              //this.products = this.products.filter((val) => !this.selectedAreas?.includes(val));
              this.selectedAreas = null;
              this.messageService.add({
                  severity: 'success',
                  summary: 'Successful',
                  detail: 'Areas Deleted',
                  life: 3000
              });
          }
      });
  }

  hideDialog() {
      this.areaDialog = false;
      this.submitted = false;
  }

  deleteArea(area: Area) {
    this.confirmationService.confirm({
      message: '¿Estas seguro que quieres eliminar el área ' + area.descripcion + '?',
      header: 'Confirmación',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        this.areaService.delete(area.id_area as number).subscribe(r => {
          this.messageService.add({ severity: 'success', summary: 'Successful', detail: 'Área eliminada', life: 3000 });
          setTimeout(() => {
            this.loadLazy({first: 0, rows: 10});
          }, 1000);
        }, e => {
          this.messageService.add({ severity: 'error', summary: 'Error', detail: e.error.message, life: 3000 });
        });
      }
    });
  }

  getSeverity(status: string) {
      switch (status) {
          case 'INSTOCK':
              return 'success';
          case 'LOWSTOCK':
              return 'warn';
          case 'OUTOFSTOCK':
              return 'danger';
          default:
              return 'info';
      }
  }

  saveArea() {
    this.submitted = true;

    if (this.area.descripcion && this.area.descripcion_completa) {
      if (this.area.id_area) {
        this.areaService.update(this.area).subscribe(r => {
          this.messageService.add({ severity: 'success', summary: 'Mensaje', detail: 'Área actualizada', life: 3000 });
          this.areaDialog = false;
          setTimeout(() => {
            this.loadLazy({first: 0, rows: 10});
          }, 1000);
        }, e => {
          this.messageService.add({ severity: 'error', summary: 'Error', detail: e.error.message, life: 3000 });
        });
      } else {
        this.areaService.save(this.area).subscribe(r => {
          this.messageService.add({ severity: 'success', summary: 'Mensaje', detail: 'Área creada', life: 3000 });
          this.areaDialog = false;
          setTimeout(() => {
            this.loadLazy({first: 0, rows: 10});
          }, 1000);
        }, e => {
          this.messageService.add({ severity: 'error', summary: 'Error', detail: e.error.message, life: 3000 });
        });
      }
    }
  }
}
