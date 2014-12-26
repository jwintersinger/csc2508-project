function q1() {
  var do_movies_share_actors = function(m1, m2, threshold) {
    m1.actors.sort();
    m2.actors.sort();

    var last_a1 = null, last_a2 = null;
    var shared_actors = 0;

    for(var i = 0; i < m1.actors.length; i++) {
      var a1 = m1.actors[i].id;
      if(a1 === last_a1)
        continue;

      for(var j = 0; j < m2.actors.length; j++) {
        var a2 = m2.actors[j].id;
        if(a2 === last_a2)
          continue;

        if(a1 === a2) {
          shared_actors++;
          if(shared_actors >= threshold) {
            return true;
          }
        }

        last_a2 = a2.id;
      }
      last_a1 = a1.id;
    }
  };

  var a = db.lol.find().map(function(doc) {
    doc.movies_with_shared_actors = db.lol.find({
      _id: { $gt: doc._id }
    }).map(function(other) {
      if(do_movies_share_actors(doc, other, 1)) {
        return other;
      } else {
        return null;
      }
    }).filter(function(candidate) {
      return candidate !== null;
    });
    return doc;
  });

  a.forEach(function(doc) {
    if(doc.movies_with_shared_actors.length === 0)
      return;
    print(doc.title);
    print(doc.movies_with_shared_actors.map(function(m) { return m.title; }));
    print();
  });
}

function q2() {
  var movies = db.lol.find({ genre: { $all: ["Action", "Adventure"] }});
  movies.forEach(function(mov) {
    print(mov.title);
  });
}

function q3() {
  var target_country = 'CA';
  var target_threshold = 0;

  db.lol.aggregate(
    {$unwind: '$reviews' },
    {$project: {
      _id: false,
      movie_id: '$title',
      in_target_country: {
        $cond: {
          if: { $eq: ['$reviews.user.country', target_country] }, then: 1, else: -1
        }
      }
    }},
    {$group: {
      _id: '$movie_id',
      review_country_sum: { $sum: '$in_target_country' }
    }},
    {$match: {review_country_sum: {$gte: target_threshold}}}
  ).forEach(function(blah) {
    printjson(blah);
  });
}

q3();
