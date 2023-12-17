import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { PopupComponent } from './popup/popup.component';
import { ResultsComponent } from './results/results.component';

const routes: Routes = [{
  path:'',component:LoginComponent
},
{
  path:'popup',component:PopupComponent
},
{
  path:'results',component:ResultsComponent
},];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
