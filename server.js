
const mysql = require('mysql');
const fs = require('fs');
const express=require("express");
const app=express();
app.use(express.urlencoded({ extended: false }));
//app.use(express.json); le programme mamchach avec
app.set('view engine', 'ejs');
app.use('/image', express.static('image'));
app.get('/pfelogin', (req, res) => {
  res.render('pfelogin'); 
});
// app.get('/', (req, res) => {
//   res.render('pfelogin');
// });

var con = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    port: 3306,
    database: "pfe1"
  });
  
  con.connect(function(err) {
    if (err) throw err;
    console.log('db ' + con.state);
  });
/* AJT_USER : */
app.post("/ajouterutilisateur",(req,res)=>{
    const {nom,prenom,email,mot_de_passe,role}=req.body;

    con.query('SELECT * FROM utilisateurs WHERE email = ?', [email], (err, results) => {
        if (err) {
          return res.status(500).send("utilisateur n'a pas pu etre identifier avant d'étre ajouté");
        }
    
        if (results.length > 0) {

          return res.status(400).send('Utilisateur avec cette email existe deja');
        } else {
    var sql = "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role) VALUES (?,?,?,?,?);";
  con.query(sql,[nom,prenom,email,mot_de_passe,role] , function (err, result) {
    if (err) {
        return res.status(500).send("utilisateur n'a pas pu etre ajouter");
      }
    console.log("utilisateur ajouter");
  });
}
    });
});

app.post("/ajouterfuite",(req,res)=>{
  fs.readFile('./scrap_result/donnees.json', 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading the file:', err);
    }else{

      const parsedData = JSON.parse(data);
    
      parsedData.forEach(item => {

    con.query('SELECT * FROM fuite WHERE information = ?', [item.titre], (err, results) => {
        if (err) {
          return res.status(500).send("la fuite n'a pas pu etre identifier avant d'étre ajouté");
        }
    
        if (results.length > 0) {

          return res.status(400).send('information existe deja');
        } else {
    var sql = "INSERT INTO fuite (information,lien,source,date) VALUES (?,?,?,?);";
  con.query(sql,[item.titre,item.lien,item.source,item.date] , function (err, result) {
    if (err) {
        return res.status(500).send("l'information n'a pas pu etre ajouter");
      }
    console.log("information ajouter");
  });
}
    });
});
}});
});

app.get("/",(req,res)=>{
  con.query("SELECT * FROM fuite", function (err, result) {
    if (err) {
        return res.status(500).send("la fuite n'a pas pu etre extrait");
      }
    res.render('index', { items: result });
  });
})
app.listen(3000,()=>{
  console.log("Server running on http://localhost:3000");
});