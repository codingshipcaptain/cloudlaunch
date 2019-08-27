import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { HttpService} from '../http.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.css']
})
export class ReviewComponent implements OnInit {
    movie: any;
    review: any;
    terr: any;
    errors: any;

    constructor(
        private _httpService: HttpService,
        private _router: Router,
        private _route: ActivatedRoute
    ){}

    ngOnInit() {
        this.movie = {};
        this.review = {};
        this._route.params.subscribe(params=> {
            console.log("Params", params);
            this._httpService.getOne(params['id']).subscribe(data => {
                this.movie = data;
            })
        })
    }

    addReview(){
        console.log("REVIEW", this.review);
        let idata = {tmovie: this.movie, treview: this.review};
        console.log("CREATE REVIEW INTAKE DATA: ", idata.treview);
        console.log("MOVIE ID: ", idata.tmovie._id)
        this._httpService.reviewAdd(idata.tmovie._id, idata).subscribe(data =>{
            if(data['good']) {
                console.log(data);
                this.movie.reviews.push(this.review);
                this._router.navigate(['/movies/'+this.movie._id])
            }
            else {
                this.errors = [];
                this.terr = data['tobj']['errors'];
                console.log("ERROR LIST", this.terr);
                if(this.terr.name != undefined){
                    if(this.terr.name.kind == 'required'){
                        this.errors.push('Name is required.');
                    }
                    if(this.terr.name.kind == 'minlength'){
                        this.errors.push('Name must be 3 or more characters.')
                    }
                }
                if(this.terr.rating != undefined){
                    if(this.terr.name.kind == 'required'){
                        this.errors.push('Rating is required.');
                    }
                }
                if(this.terr.ureview != undefined){
                    if(this.terr.ureview.kind == 'required'){
                        this.errors.push('Review is required.');
                    }
                    if(this.terr.ureview.kind == 'minlength'){
                        this.errors.push('Review must be 3 or more characters.')
                    }
                }
                if(this.terr.title != undefined){
                    if(this.terr.title.kind == 'required'){
                        this.errors.push('Title is required.');
                    }
                    if(this.terr.title.kind == 'minlength'){
                        this.errors.push('Title must be 3 or more characters.')
                    }
                }
            }
        });
    }

    cancel(){this._router.navigate(['/movies'])}

}
