from django.db import models
from django.core import validators

class CssColor(models.Model):
    name = models.CharField(unique=True,max_length=1024)
    hexadecimal=models.CharField(max_length=6,blank=True,
                                 validators=[validators.MinLengthValidator(6),
                                             validators.RegexValidator(regex=r'^[0-9abcdefABCDEF]+$')])
    red = models.PositiveIntegerField(validators=[validators.MinValueValidator(0),
                                                  validators.MaxValueValidator(255)],blank=True)
    green = models.PositiveIntegerField(validators=[validators.MinValueValidator(0),
                                                    validators.MaxValueValidator(255)],blank=True)
    blue = models.PositiveIntegerField(validators=[validators.MinValueValidator(0),
                                                   validators.MaxValueValidator(255)],blank=True)
    
    def save(self,*args,**kwargs):
        if self.id==0:
            self.red=0
            self.green=0
            self.blue=0
            self.hexadecimal=""
            super(CssColor, self).save(*args, **kwargs)
            return
        if not self.red: self.red=0
        if not self.green: self.green=0
        if not self.blue: self.blue=0
        if not self.hexadecimal:
            self.hexadecimal="%2.2x%2.2x%2.2x" % (self.red,self.green,self.blue)
        else:
            r=self.hexadecimal[0:2]
            g=self.hexadecimal[2:4]
            b=self.hexadecimal[4:6]
            self.red=int(r,16)
            self.green=int(g,16)
            self.blue=int(b,16)
        super(CssColor, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.name)

    def rgb(self):
        if self.id==0:
            return u"transparent"
        U= u"%d,%d,%d" % (self.red,self.green,self.blue)
        return U

    class Meta:
        ordering = [ "name" ]

class CssColorVariable(models.Model):
    name = models.SlugField(unique=True)
    color = models.ForeignKey(CssColor)
    alpha = models.FloatField(validators=[validators.MinValueValidator(0.0),
                                          validators.MaxValueValidator(1.0)],
                              default=1.0)

    class Meta:
        ordering = [ "name" ]

    def save(self,*args,**kwargs):
        self.name=self.name.upper()
        super(CssColorVariable, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.color.id==0:
            return u"transparent"
        U=u"rgb"
        if self.alpha!=1.0:
            U+=u"a"
        U+= u"(%s" % self.color.rgb()
        if self.alpha!=1.0:
            U+=u",%2.2f" % self.alpha
        U+=u")"
        return U

class CssShadow(models.Model):
    h_shadow = models.CharField(max_length=1024)
    v_shadow = models.CharField(max_length=1024)
    blur = models.CharField(max_length=1024)
    spread = models.CharField(max_length=1024)

    def __unicode__(self):
        U=self.h_shadow+u" "+self.v_shadow+u" "+self.blur+u" "+self.spread
        return U

    def save(self,*args,**kwargs):
        super(CssShadow, self).save(*args, **kwargs)

class CssShadowVariable(models.Model):
    name = models.CharField(unique=True,max_length=1024)
    shadows = models.ManyToManyField(CssShadow,through='CssShadowThrough')

    class Meta:
        ordering = [ "name" ]

    def save(self,*args,**kwargs):
        self.name=self.name.upper()
        super(CssShadowVariable, self).save(*args, **kwargs)

    def __unicode__(self):
        U=[]
        for rel in self.cssshadowthrough_set.all():
            U.append( unicode(rel) )
        return u", ".join(U)

class CssShadowThrough(models.Model):
    variable = models.ForeignKey(CssShadowVariable)
    shadow = models.ForeignKey(CssShadow)
    color = models.ForeignKey(CssColor)
    alpha = models.FloatField(validators=[validators.MinValueValidator(0.0),
                                          validators.MaxValueValidator(1.0)],
                              default=1.0)
    inset = models.BooleanField(default=False)
    
        
    def __unicode__(self):
        if self.color.id==0:
            return u"none"
        U=unicode(self.shadow)
        U+=u" rgb"
        if self.alpha!=1.0:
            U+=u"a"
        U+= u"(%s" % self.color.rgb()
        if self.alpha!=1.0:
            U+=u",%2.2f" % self.alpha
        U+=u")"
        if self.inset:
            U+=u" inset"
        return U

class CssEquivalence(models.Model):
    name = models.CharField(unique=True,max_length=1024)

    def __unicode__(self): return self.name

class CssEquivalenceStyle(models.Model):
    name = models.CharField(unique=True,max_length=1024)

    def __unicode__(self): return self.name

class CssEquivalenceColor(models.Model):
    equivalence = models.ForeignKey(CssEquivalence)
    style = models.ForeignKey(CssEquivalenceStyle)
    color = models.ForeignKey(CssColor)

    class Meta:
        unique_together = ("equivalence","style")
    
    def __unicode__(self): return unicode(self.style)+" "+unicode(self.equivalence)

class CssEquivalenceColorVariable(models.Model):
    name = models.SlugField(unique=True)
    equivalence = models.ForeignKey(CssEquivalence)
    alpha = models.FloatField(validators=[validators.MinValueValidator(0.0),
                                          validators.MaxValueValidator(1.0)],
                              default=1.0)

    def __unicode__(self):
        U=unicode(self.name)+": "+unicode(self.equivalence)+" (alpha="+("%2.2f" % self.alpha)+")"
        return U

    def save(self,*args,**kwargs):
        self.name=self.name.upper()
        super(CssEquivalenceColorVariable, self).save(*args, **kwargs)

    def color_desc(self,color):
        if color.id==0:
            return u"transparent"
        U=u"rgb"
        if self.alpha!=1.0:
            U+=u"a"
        U+= u"(%s" % color.rgb()
        if self.alpha!=1.0:
            U+=u",%2.2f" % self.alpha
        U+=u")"
        return U
