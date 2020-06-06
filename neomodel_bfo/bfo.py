from neomodel import (config,
                      StructuredNode,
                      StringProperty,
                      UniqueIdProperty)


class Entity(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=False)


class Continuant(Entity): pass


class IndependentContinuant(Continuant): pass


class MaterialEntity(IndependentContinuant): pass


class Object(MaterialEntity): pass


class FiatObjectPart(MaterialEntity): pass


class ObjectAggregate(MaterialEntity): pass


class ImmaterialEntity(IndependentContinuant): pass


class Site(ImmaterialEntity): pass


class ContinuantFiatBoundary(ImmaterialEntity): pass


class ZeroDimensionalContinuantFiatBoundary(ContinuantFiatBoundary): pass


class OneDimensionalContinuantFiatBoundary(ContinuantFiatBoundary): pass


class TwoDimensionalContinuantFiatBoundary(ContinuantFiatBoundary): pass


class SpatialRegion(ImmaterialEntity): pass


class ZeroDimensionalSpatialRegion(SpatialRegion): pass


class OneDimensionalSpatialRegion(SpatialRegion): pass


class TwoDimensionalSpatialRegion(SpatialRegion): pass


class ThreeDimensionalSpatialRegion(SpatialRegion): pass


class GenericallyDependentContinuant(Continuant): pass


class SpecificallyDependentContinuant(Continuant): pass


class Quality(SpecificallyDependentContinuant): pass


class RelationalQuality(Quality): pass


class RealizableEntity(SpecificallyDependentContinuant): pass


class Role(RealizableEntity): pass


class Disposition(RealizableEntity): pass


class Function(Disposition): pass


class Occurrent(Entity): pass


class Process(Occurrent): pass


class History(Process): pass


class ProcessProfile(Process): pass


class ProcessBoundary(Occurrent): pass


class TemporalRegion(Occurrent): pass


class ZeroDimensionalTemporalRegion(TemporalRegion): pass


class OneDimensionalTemporalRegion(TemporalRegion): pass


class SpatioTemporalRegion(Occurrent): pass


if __name__ == '__main__':
    pass
