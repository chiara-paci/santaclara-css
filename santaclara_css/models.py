from django.db import models
from django.core import validators
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError


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
        key="COLOR_"+unicode(self.name)
        value=unicode(self)
        CssVariable.objects.mk_variable(key,value)

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

    class Meta:
        unique_together = ("h_shadow","v_shadow","blur","spread")
        ordering = ("h_shadow","v_shadow","blur","spread")

    def __unicode__(self):
        U=self.h_shadow+u" "+self.v_shadow+u" "+self.blur+u" "+self.spread
        return U

    def shadow_text(self):
        U=self.h_shadow+u" "+self.v_shadow+u" "+self.blur
        return U

    def save(self,*args,**kwargs):
        super(CssShadow, self).save(*args, **kwargs)

class CssShadowVariable(models.Model):
    name = models.CharField(unique=True,max_length=1024)
    shadows = models.ManyToManyField(CssShadow,through='CssShadowThrough')
    shadow_text = models.BooleanField(default=False)

    class Meta:
        ordering = [ "name" ]

    def save(self,*args,**kwargs):
        self.name=self.name.upper()
        super(CssShadowVariable, self).save(*args, **kwargs)
        key="SHADOW_"+unicode(self.name)
        value=unicode(self)
        CssVariable.objects.mk_variable(key,value)

    def __unicode__(self):
        U=[]
        if self.shadow_text:
            for rel in self.cssshadowthrough_set.all():
                U.append( rel.shadow_text() )
        else:
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

    def shadow_text(self):
        if self.color.id==0:
            return u"none"
        U=self.shadow.shadow_text()
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

    class Meta:
        ordering = [ "name" ]

class CssEquivalenceStyle(models.Model):
    name = models.CharField(unique=True,max_length=1024)

    def __unicode__(self): return self.name

    class Meta:
        ordering = [ "name" ]

class CssEquivalenceColor(models.Model):
    equivalence = models.ForeignKey(CssEquivalence)
    style = models.ForeignKey(CssEquivalenceStyle)
    color = models.ForeignKey(CssColor)

    class Meta:
        unique_together = ("equivalence","style")
        ordering = ("equivalence",)
    
    def __unicode__(self): return unicode(self.style)+" "+unicode(self.equivalence)

class CssEquivalenceColorVariable(models.Model):
    name = models.SlugField(unique=True)
    equivalence = models.ForeignKey(CssEquivalence)
    alpha = models.FloatField(validators=[validators.MinValueValidator(0.0),
                                          validators.MaxValueValidator(1.0)],
                              default=1.0)

    class Meta:
        ordering = [ "name" ]

    def __unicode__(self):
        U=unicode(self.name)+": "+unicode(self.equivalence)+" (alpha="+("%2.2f" % self.alpha)+")"
        return U

    def save(self,*args,**kwargs):
        self.name=self.name.upper()
        super(CssEquivalenceColorVariable, self).save(*args, **kwargs)
        name=unicode(self.name)
        for style,color in self.color_dict():
            key="COLOR_"+style.upper()+"_"+name
            value=color
            CssVariable.objects.mk_variable(key,value)

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

    def color_dict(self):
        T={}
        for eq_color in self.equivalence.cssequivalencecolor_set.all():
            style=unicode(eq_color.style)
            T[style]=self.color_desc(eq_color.color)
        return T.items()

class CssEquivalenceShadowVariable(models.Model):
    name = models.CharField(unique=True,max_length=1024)
    shadows = models.ManyToManyField(CssShadow,through='CssEquivalenceShadowThrough')
    shadow_text = models.BooleanField(default=False)

    class Meta:
        ordering = [ "name" ]

    def save(self,*args,**kwargs):
        self.name=self.name.upper()
        super(CssEquivalenceShadowVariable, self).save(*args, **kwargs)
        name=unicode(self.name)
        for style,shadow in self.shadow_dict():
            key="SHADOW_"+style.upper()+"_"+name
            value=shadow
            CssVariable.objects.mk_variable(key,value)

    def __unicode__(self):
        U=[]
        if self.shadow_text:
            for rel in self.cssequivalenceshadowthrough_set.all():
                U.append( rel.shadow_text() )
        else:
            for rel in self.cssequivalenceshadowthrough_set.all():
                U.append( unicode(rel) )
        return unicode(self.name)+u": "+u", ".join(U)

    def shadow_dict(self):
        T={}
        for eq_shadow in self.cssequivalenceshadowthrough_set.all():
            for eq_color in eq_shadow.equivalence.cssequivalencecolor_set.all():
                style=unicode(eq_color.style)
                if not T.has_key(style):
                    T[style]=[]
                T[style].append(eq_shadow.shadow_desc(eq_color.color,self.shadow_text))
        R=[]
        for style,shadow_list in T.items():
            R.append( (style,",".join(shadow_list)) )
        return R

class CssEquivalenceShadowThrough(models.Model):
    variable = models.ForeignKey(CssEquivalenceShadowVariable)
    shadow = models.ForeignKey(CssShadow)
    equivalence = models.ForeignKey(CssEquivalence)
    alpha = models.FloatField(validators=[validators.MinValueValidator(0.0),
                                          validators.MaxValueValidator(1.0)],
                              default=1.0)
    inset = models.BooleanField(default=False)
    

    class Meta:
        ordering = [ "variable" ]

    def save(self,*args,**kwargs):
        super(CssEquivalenceShadowThrough, self).save(*args, **kwargs)
        name=unicode(self.variable.name)
        for style,shadow in self.variable.shadow_dict():
            key="SHADOW_"+style.upper()+"_"+name
            value=shadow
            CssVariable.objects.mk_variable(key,value)

        
    def shadow_desc(self,color,is_shadow_text):
        if is_shadow_text:
            U=self.shadow.shadow_text()
        else:
            U=unicode(self.shadow)
        U+=" "
        if color.id==0:
            U+=u"transparent"
            if self.inset:
                U+=u" inset"
            return U
        U+=u"rgb"
        if self.alpha!=1.0:
            U+=u"a"
        U+= u"(%s" % color.rgb()
        if self.alpha!=1.0:
            U+=u",%2.2f" % self.alpha
        U+=u")"
        if self.inset:
            U+=u" inset"
        return U

    def __unicode__(self):
        U=unicode(self.shadow)+" "+unicode(self.equivalence)+" (alpha="+("%2.2f" % self.alpha)+")"
        if self.inset:
            U+=u" inset"
        return U

    def shadow_text(self):
        U=self.shadow.shadow_text()+" "+unicode(self.equivalence)+" (alpha="+("%2.2f" % self.alpha)+")"
        if self.inset:
            U+=u" inset"
        return U

class CssVariableManager(models.Manager):
    def mk_variable(self,key,value):
        var_obj,created=self.get_or_create(key=key,defaults={"value":value})
        if not created:
            var_obj.value=value
            var_obj.save()
        return var_obj,created

class CssVariable(models.Model):
    key = models.CharField(unique=True,max_length=2048)
    value = models.CharField(max_length=2048)
    objects = CssVariableManager()

    def __unicode__(self):
        return unicode(self.key)+u": "+unicode(self.value)

    class Meta:
        ordering = [ "key" ]

###########

class CssEquivalenceBorder(models.Model):
    width = models.CharField(max_length=128,default="1px")
    color = models.ForeignKey(CssEquivalenceColorVariable)
    style = models.CharField(max_length=128,default='solid',choices = ( ( "dotted", "dotted" ),
                                                                        ( "dashed", "dashed" ),
                                                                        ( "solid", "solid" ),
                                                                        ( "double", "double" ),
                                                                        ( "groove", "groove" ),
                                                                        ( "ridge", "ridge" ),
                                                                        ( "inset", "inset" ),
                                                                        ( "outset", "outset" ) ) )
    
    def __unicode__(self):
        U=unicode(self.width)+" "+unicode(self.style)+" "+unicode(self.color.name)
        return U
    
class CssEquivalenceLinearGradient(models.Model):
    direction =  models.CharField( max_length=128, default="top")
    colors = models.ManyToManyField(CssEquivalenceColorVariable,through='CssEquivalenceLinearGradientThrough')

    def __unicode__(self):
        U=unicode(self.direction)
        for color in self.colors.all():
            U+=u" "+unicode(color.name)
        return U

class CssEquivalenceLinearGradientThrough(models.Model):
    color = models.ForeignKey(CssEquivalenceColorVariable)
    gradient = models.ForeignKey(CssEquivalenceLinearGradient)
    pos = models.PositiveIntegerField()

    class Meta:
        ordering = [ "pos" ]

class CssEquivalenceSelector(models.Model):
    selector = models.CharField(max_length=1024)

    def __unicode__(self): return unicode(self.selector)

class CssEquivalenceStanza(models.Model):
    selectors = models.ManyToManyField(CssEquivalenceSelector)
    box_shadow = models.ManyToManyField(CssEquivalenceShadowVariable,blank=True,through=CssEquivalenceStanzaBoxShadowThrough)
    borders = models.ManyToManyField(CssEquivalenceBorder,blank=True,through=CssEquivalenceStanzaBorderThrough)
    colors = models.ManyToManyField(CssEquivalenceColorVariable,blank=True,through=CssEquivalenceStanzaColorThrough)
    linear_gradients = models.ManyToManyField(CssEquivalenceLinearGradient,blank=True,through=CssEquivalenceStanzaLinearGradientThrough)
    
    def __unicode__(self): 
        U=u""
        sep=u""
        for sel in self.selectors.all():
            U+=sep+unicode(sel)
            sep=u", "
        return U

class CssEquivalenceStanzaBoxShadowThrough(models.Model):
    stanza = models.ForeignKey(CssEquivalenceStanza)
    shadow = models.ForeignKey(CssEquivalenceShadowVariable)

    class Meta:
        unique_together = [ "stanza","shadow" ]
    
class CssEquivalenceStanzaBorderThrough(models.Model):
    stanza = models.ForeignKey(CssEquivalenceStanza)
    border = models.ForeignKey(CssEquivalenceBorder)
    position = models.CharField(max_length=128,choices=( ( "left","left" ),
                                                         ( "top", "top" ),
                                                         ( "right", "right" ),
                                                         ( "bottom", "bottom" ) ) )

    class Meta:
        unique_together = [ "stanza","border","position" ]
    
class CssEquivalenceStanzaBoxShadowThrough(models.Model):
    stanza = models.ForeignKey(CssEquivalenceStanza)
    color = models.ForeignKey(CssEquivalenceColorVariable)
    target = models.CharField(max_length=128,choices = ( ( "back","back" ),
                                                         ( "fore", "fore" ) ) )

    class Meta:
        unique_together = [ "stanza","color","target" ]


class CssEquivalenceStanzaLinearGradientThrough(models.Model):
    stanza = models.ForeignKey(CssEquivalenceStanza)
    gradient = models.ForeignKey(CssEquivalenceLinearGradient)
    target = models.CharField(max_length=128,choices = ( ( "back","back" ) )

    class Meta:
        unique_together = [ "stanza","gradient","target" ]
    
