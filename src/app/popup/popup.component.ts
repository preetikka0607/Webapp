import { Component, OnInit } from '@angular/core';
import {MatSnackBar} from '@angular/material/snack-bar';
import { HttpClientModule } from '@angular/common/http';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-popup',
  templateUrl: './popup.component.html',
  styleUrls: ['./popup.component.css']
})
export class PopupComponent implements OnInit {
  file:File;
  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }
  getFile(event:any){
    this.file=event.target.files[0];      
    console.log('file', this.file);    
  }    
  uploadFile(): void {      
    let formData=new FormData();      
    formData.set("file",this.file);      
    this.http.post('http://127.0.0.1:5000', formData).subscribe((response)=>{});     }


}
 